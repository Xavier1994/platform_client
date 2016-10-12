# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
from requests.auth import AuthBase

from .exceptions import PlatformAuthFailedError


class NoneAuth(AuthBase):

    def __init__(self, *args, **kwargs):
        return

    def __call__(self, r):
        return r


class PlatformAuth(AuthBase):

    session_id = None
    username = None
    password = None
    login_url = None

    def __init__(self,
                 username=None,
                 password=None,
                 login_url='http://127.0.0.1:7500/resource_manager/user/login'):
        same_user = (PlatformAuth.username == username) and \
                    (PlatformAuth.password == password) and \
                    (PlatformAuth.login_url == login_url)

        PlatformAuth.username, PlatformAuth.password, PlatformAuth.login_url = username, password, login_url

        # if user is not login or user setting changed, just login again
        if (PlatformAuth.session_id is None) or (not same_user):
            self._login()

    def _login(self):
        data = {'name': PlatformAuth.username,
                'password': PlatformAuth.password}

        try:
            r = requests.post(url=PlatformAuth.login_url,
                              json=data)
        except:
            raise PlatformAuthFailedError('username: ' + PlatformAuth.username)

        response = r.json()
        PlatformAuth.session_id = response.get('session_id')

    def __call__(self, r):
        if PlatformAuth.session_id is None:
            raise PlatformAuthFailedError(PlatformAuth.username)

        r.headers['session_id'] = PlatformAuth.session_id
        return r
