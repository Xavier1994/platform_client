# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import unitetst2 as unittest
except ImportError:
    import unittest

import json
import requests_mock

from platform_client.client import PlatformClient
from platform_client.exceptions import PlatformInvalidUrlError
from platform_client.exceptions import PlatformClientError
from platform_client.exceptions import PlatformServerError


class TestPlatformClient(unittest.TestCase):

    def setUp(self):
        self.cli = PlatformClient(host='192.168.0.1',
                                  port=7500,
                                  username='system',
                                  password='YituTech837')

    def test_validate_service(self):
        self.cli.validate_service('sync_import_image')

        with self.assertRaises(PlatformInvalidUrlError):
            self.cli.validate_service('fuck')

    def test_request(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:7500/resource_manager/user/login',
                status_code=200,
                json={'session_id': 1234}
            )
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:80/fuck',
                status_code=200,
                headers={'Content-Type': 'application/json'},
                json={'result': 'fuck'}
            )

            r = self.cli.request(url='http://192.168.0.1:80/fuck')
            result_body = r.json()
            self.assertDictEqual(result_body, {'result': 'fuck'})
            self.assertEqual(m.last_request.headers['session_id'], 1234)

    def test_service_normal(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:7500/resource_manager/user/login',
                status_code=200,
                json={'session_id': 1234}
            )
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:9110/car/picture/synchronized',
                status_code=200,
                headers={'Content-Type': 'application/json'},
                json={'rtn': 0, 'message': 'OK', 'result': []}
            )

            r = self.cli.sync_import_image(repository_id=1,
                                           picture_image_content_base64='xxx')
            result_body = r.json()
            expected_dict = {'rtn': 0, 'message': 'OK', 'result': []}
            self.assertDictEqual(expected_dict, result_body)
            request_body = json.loads(m.last_request.body)
            expected_dict = {'repository_id': 1,
                             'picture_image_content_base64': 'xxx'}
            self.assertDictEqual(expected_dict, request_body)

    def test_service_complicated_data_type(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:7500/resource_manager/user/login',
                status_code=200,
                json={'session_id': 1234}
            )
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:9110/car/picture/synchronized',
                status_code=200,
                headers={'Content-Type': 'application/json'},
                json={'rtn': 0, 'message': 'OK', 'result': []}
            )
            self.cli.sync_import_image(image={'content': 'xxx', 'id': 1234},
                                       name='fuck',
                                       extra=['shit1', 'shit2'])
            expected_dict = {'image': {'content': 'xxx', 'id': 1234},
                             'name': 'fuck',
                             'extra': ['shit1', 'shit2']}
            request_body = json.loads(m.last_request.body)
            self.assertDictEqual(expected_dict, request_body)

    def test_service_with_header(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:7500/resource_manager/user/login',
                status_code=200,
                json={'session_id': 1234}
            )
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:9110/car/picture/synchronized',
                status_code=200,
                headers={'Content-Type': 'application/json'},
                json={'rtn': 0, 'message': 'OK', 'result': []}
            )
            self.cli.sync_import_image(_headers={'what': 'fuck you',
                                                 'why': 'you are a shit'},
                                       repository_id=1,
                                       image_content='xxx')
            self.assertEqual(m.last_request.headers['what'], 'fuck you')
            self.assertEqual(m.last_request.headers['why'], 'you are a shit')
            self.assertDictEqual(json.loads(m.last_request.body),
                                 {'repository_id': 1, 'image_content': 'xxx'})

    def test_service_with_params(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:7500/resource_manager/user/login',
                status_code=200,
                json={'session_id': 1234}
            )
            m.register_uri(
                requests_mock.GET,
                'http://192.168.0.1:9900/car/v1/framework/car_video/camera',
                status_code=200,
                headers={'Content-Type': 'application/json'},
                json={'rtn': 0, 'message': 'OK'}
            )
            r = self.cli.get_camera(_params={'what': 'shit'})
            self.assertEqual(r.status_code, 200)
            self.assertDictEqual(r.json(), {'rtn': 0, 'message': 'OK'})
            self.assertEqual(r.url,
                             'http://192.168.0.1:9900/car/v1/framework/car_video/camera?what=shit')

    def test_validate_service_error(self):
        with self.assertRaises(PlatformInvalidUrlError):
            self.cli.haha()

    def test_client_error(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:7500/resource_manager/user/login',
                status_code=200,
                json={'session_id': 1234}
            )
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:9110/car/picture/synchronized',
                status_code=404
            )
            with self.assertRaises(PlatformClientError):
                self.cli.sync_import_image(what='fuck')

    def test_service_error(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:7500/resource_manager/user/login',
                status_code=200,
                json={'session_id': 1234}
            )
            m.register_uri(
                requests_mock.POST,
                'http://192.168.0.1:9110/car/picture/synchronized',
                status_code=500
            )
            with self.assertRaises(PlatformServerError):
                self.cli.sync_import_image(what='fuck')
