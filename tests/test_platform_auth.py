# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import unitetst2 as unittest
except ImportError:
    import unittest

import requests
import requests_mock

from platform_client.platform_auth import PlatformAuth


class TestPlatformAuth(unittest.TestCase):

    def test_init_auth_object(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://127.0.0.1:7500/resource_manager/user/login',
                status_code=200,
                text='{"session_id": 1234}'
            )

            r = requests.Request()
            cli = PlatformAuth()
            r = cli(r)
            self.assertEqual(1234, r.headers['session_id'])

    def test_not_login_again(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://127.0.0.1:7500/resource_manager/user/login',
                status_code=200,
                text='{"session_id": 1234}'
            )

            r = requests.Response()
            cli = PlatformAuth(username='magician',
                               password='fuck')
            r = cli(r)
            self.assertEqual(1234, r.headers['session_id'])
            m.register_uri(
                requests_mock.POST,
                'http://127.0.0.1:7500/resource_manager/user/login',
                status_code=200,
                text='{"session_id": 4567}'
            )
            cli = PlatformAuth(username='magician',
                               password='fuck')
            r = cli(r)
            self.assertEqual(1234, r.headers['session_id'])

    def test_login_again(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://127.0.0.1:7500/resource_manager/user/login',
                status_code=200,
                text='{"session_id": 1234}'
            )

            r = requests.Response()
            cli = PlatformAuth(username='shit2',
                               password='fuck2')
            r = cli(r)
            self.assertEqual(1234, r.headers['session_id'])
            m.register_uri(
                requests_mock.POST,
                'http://127.0.0.1:7500/resource_manager/user/login',
                status_code=200,
                text='{"session_id": 4567}'
            )
            cli = PlatformAuth(username='shit',
                               password='fuck')
            r = cli(r)
            self.assertEqual(4567, r.headers['session_id'])
