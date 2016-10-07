"""
Python client for Yitu Platform
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .constants import CONST
from .exceptions import PlatformInvalidAccessMethodError


class ServiceInstance(object):

    def __init__(self,
                 url=None,
                 port=80,
                 access_method='POST'):
        self._url = str(url)
        self._port = int(port)

        if access_method not in CONST.METHODS:
            raise PlatformInvalidAccessMethodError(access_method)

        self._access_method = str(access_method)

        self._access_url = ":{0}{1}".format(
            self._port,
            self._url
        )

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = int(new_port)

        self._access_url = ":{0}{1}".format(
            self.port,
            self.url
        )

    @property
    def access_url(self):
        return self._get_access_url()

    def _get_access_url(self):
        return self._access_url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url):
        self._url = str(new_url)

        self._access_url = ":{0}{1}".format(
            self.port,
            self.url
        )

    @property
    def access_method(self):
        return self._access_method

    @access_method.setter
    def access_method(self, new_method):
        if new_method not in CONST.METHODS:
            raise PlatformInvalidAccessMethodError(new_method)
        self._access_method = new_method

    def __str__(self):
        return str(
            {
                'port': self._port,
                'method': self._access_method,
                'url': self._url
            })


class ServiceLib(object):

    def __init__(self, services):
        self._services = services

    def has_service(self, name):
        return (name in self._services)

    def get_service_instance(self, service_name):
        return self._services.get(service_name)

    def __str__(self):
        return str(self._services)
