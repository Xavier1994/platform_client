# -*- coding: utf-8 -*-
"""
Python client for Platform Http Service
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import requests
import requests.exceptions

from .platform_auth import PlatformAuth
from .default_lib import default_service_lib
from .exceptions import PlatformClientError
from .exceptions import PlatformServerError
from .exceptions import PlatformInvalidUrlError


try:
    xrange
except NameError:
    xrange = range


class PlatformClient(object):
    """The :class:`~.PlatformClient` object holds information necessary to
    ask service for platform. Requests can be made to platform directly through
    the client

    :param host: hostname to connect to Platform, defaults to 'localhost'
    :type host: str
    :param port: port to connect to Platform, defaults to 8086
    :type port: int
    :param username: user to connect, defaults to 'root'
    :type username: str
    :param password: password of the user, defaults to 'root'
    :type password: str
    :param timeout: number of second requests wait for response
    :type timeout: int
    :param ssl: use https instead of http to connect to InfluxDB, defaults to
    ┊   False
    :type ssl: bool
    :param verify_ssl: verify SSL certificates for HTTPS requests, defaults to
    ┊   False
    :type verify_ssl: bool
    :param services: services the user define use ServiceInstance
    :type services: ServiceLib
    """

    def __init__(self,
                 host='localhost',
                 port=7500,
                 username='root',
                 password='root',
                 timeout=None,
                 ssl=False,
                 verify_ssl=False,
                 services=default_service_lib,
                 auth=PlatformAuth
                 ):
        """Construct a new Platform object."""
        self.__host = host
        self.__port = int(port)
        self._username = username
        self._password = password
        self._timeout = timeout
        self._auth = auth

        self._session = requests.Session()

        self._ssl = ssl
        self._verify_ssl = verify_ssl

        self._services = services

        self._scheme = "http"
        if ssl is True:
            self._scheme = "https"

        self.__baseurl = "{0}://{1}".format(
            self._scheme,
            self._host)

        # TODO(Wei.Xie) hard code here, make it flexiable
        self._base_login_url = "{0}://{1}:{2}/{3}".format(
            self._scheme,
            self._host,
            self._port,
            'resource_manager/user/login'
        )

        self._headers = {
            'Content-type': 'application/json',
            'Accept': '*'
        }

    @property
    def _baseurl(self):
        return self._get_baseurl()

    def _get_baseurl(self):
        return self.__baseurl

    @property
    def _host(self):
        return self._get_host()

    def _get_host(self):
        return self.__host

    @property
    def _port(self):
        return self._get_port()

    def _get_port(self):
        return self.__port

    def validate_service(self, service_name):
        if not self._services.has_service(service_name):
            raise PlatformInvalidUrlError(service_name)

    def request(self, url, method='POST', params=None, data=None,
                expected_response_code=200, headers=None):
        """Make a HTTP request to the Platform API.

        :param url: the path of the HTTP request, e.g. write, query, etc.
        :type url: str
        :param method: the HTTP method for the request, defaults to GET
        :type method: str
        :param params: additional parameters for the request, defaults to None
        :type params: dict
        :param data: the data of the request, defaults to None
        :type data: str
        :param expected_response_code: the expected response code of
            the request, defaults to 200
        :type expected_response_code: int
        :returns: the response from the request
        :rtype: :class:`requests.Response`
        """

        if headers is None:
            headers = self._headers

        if params is None:
            params = {}

        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        # TODO(Wei Xie) make it configurable
        for i in range(0, 3):
            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    auth=self._auth(self._username,
                                    self._password,
                                    self._base_login_url),
                    params=params,
                    data=data,
                    headers=headers,
                    timeout=self._timeout
                )
                break
            except requests.exceptions.ConnectionError as e:
                if i < 2:
                    continue
                else:
                    raise e

        if response.status_code >= 500 and response.status_code < 600:
            raise PlatformServerError(response.content)
        elif response.status_code == expected_response_code:
            return response
        else:
            raise PlatformClientError(response.content, response.status_code)

    def get_service(self, service_name, headers=None, params=None, body=None):
            self.validate_service(service_name)

            service_instance = self._services.get_service_instance(
                service_name
            )

            method = service_instance.access_method
            url = self._baseurl + service_instance.access_url

            return self.request(url=url,
                                method=method,
                                headers=headers,
                                params=params,
                                data=json.dumps(body))

    def dispatch_service(self,
                         _service_name,
                         _headers=None,
                         _params=None,
                         *args,
                         **kwargs):
        """Dispatch servies to Platform Server

        :param _service_name: the name of service, eg. sync_import_image
        :type url: str
        :param _headers: http headers
        :type _headers: dict
        :param _params: http params for get request
        :type _params: dict
        :returns: the response from the request
        :rtype: :class:`requests.Response`
        """
        self.validate_service(_service_name)

        service_instance = self._services.get_service_instance(_service_name)
        method = service_instance.access_method
        url = self._baseurl + service_instance.access_url

        return self.request(url=url,
                            method=method,
                            headers=_headers,
                            params=_params,
                            data=json.dumps(kwargs))

    def __enter__(self):
        return self

    def __exit__(self):
        # reset auth session id, make login again
        self.auth.session_id = None

    def __getattr__(self, attr):
        def wrapper(*args, **kwargs):
            return self.dispatch_service(_service_name=attr, *args, **kwargs)

        return wrapper
