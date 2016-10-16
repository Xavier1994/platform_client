# -*- coding: utf-8 -*-
"""
Python client for Platform Http Service
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import functools
import requests
import requests.exceptions

from .platform_auth import PlatformAuth
from .platform_auth import NoneAuth
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
    :param service_lib: service_lib the user define use ServiceInstance
    :type service_lib: ServiceLib
    """

    def __init__(self,
                 host='localhost',
                 port=7500,
                 username='system',
                 password='YituTech837',
                 timeout=None,
                 ssl=False,
                 verify_ssl=False,
                 service_lib=default_service_lib,
                 auth=PlatformAuth
                 ):
        """Construct a new Platform object."""
        self.__host = host
        self.__port = int(port)
        self._username = username
        self._password = password
        self._timeout = timeout
        self._auth = auth or NoneAuth

        self._session = requests.Session()

        self._ssl = ssl
        self._verify_ssl = verify_ssl

        self._service_lib = service_lib

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
    def service_lib(self):
        return self._service_lib

    @service_lib.setter
    def service_lib(self, value):
        self._service_lib = value

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

    def _validate_service(self, service_name):
        if not self._service_lib.has_service(service_name):
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

    def get_service_list(self):
        return self._service_lib.get_service_list()

    def get_service(self, service_name, headers=None, params=None, body=None):
            self._validate_service(service_name)

            service_instance = self._service_lib.get_service_instance(
                service_name
            )

            method = service_instance.access_method
            url = self._baseurl + service_instance.access_url

            return self.request(url=url,
                                method=method,
                                headers=headers,
                                params=params,
                                data=json.dumps(body))

    def _dispatch_service(self,
                          _service_name,
                          _headers=None,
                          _params=None,
                          _body={},
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
        self._validate_service(_service_name)

        service_instance = self._service_lib.get_service_instance(_service_name)
        method = service_instance.access_method
        url = self._baseurl + service_instance.access_url
        _body.update(kwargs)

        return self.request(url=url,
                            method=method,
                            headers=_headers,
                            params=_params,
                            data=json.dumps(_body))

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        # reset auth session id, make login again
        if hasattr(self._auth, 'session_id'):
            self._auth.session_id = None

    def __getattr__(self, attr):
        return functools.partial(self._dispatch_service, _service_name=attr)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped_function(*args, **kwargs):
            global_vars = func.__globals__
            ori_globals = global_vars.copy()
            for name in self.get_service_list():
                global_vars[name] = functools.partial(self._dispatch_service,
                                                      _service_name=name)
            result = func(*args, **kwargs)
            global_vars = ori_globals
            return result
        return wrapped_function
