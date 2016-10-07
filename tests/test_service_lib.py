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

from platform_client.service_lib import ServiceInstance, ServiceLib
from platform_client.exceptions import PlatformInvalidAccessMethodError


class TestServiceLib(unittest.TestCase):

    def setUp(self):
        services = {}
        sync_image_service = ServiceInstance(url='/sync_image',
                                             port=1000,
                                             access_method='POST')
        async_image_service = ServiceInstance(url='/async_image',
                                              port=2000)
        services['sync'] = sync_image_service
        services['async'] = async_image_service

        self.service_lib = ServiceLib(services)

    def test_default_service(self):
        service_instance = ServiceInstance()
        self.assertEqual(service_instance.port, 80)
        self.assertEqual(service_instance.access_method, 'POST')

    def test_property(self):
        service_instance = ServiceInstance(url='/test',
                                           port=1000,
                                           access_method='GET')

        self.assertEqual(service_instance.port, 1000)
        self.assertEqual(service_instance.url, '/test')
        self.assertEqual(service_instance.access_method, 'GET')
        self.assertEqual(service_instance.access_url, ':1000/test')

        service_instance.port = 2000
        self.assertEqual(service_instance.port, 2000)
        self.assertEqual(service_instance.access_url, ':2000/test')

    def test_service_instance_init_invalid_method(self):
        with self.assertRaises(PlatformInvalidAccessMethodError):
            ServiceInstance(access_method='FUCK')

    def test_set_invalid_method(self):
        service_instance = ServiceInstance()

        try:
            service_instance.access_method = 'PATCH'
        except PlatformInvalidAccessMethodError:
            self.assertEqual(0, 0)
        except:
            self.assertEqual(0, 1)

    @unittest.skip("fucking skipping")
    def test_service_instance_str(self):
        service_instance = ServiceInstance(url='fuck')

        expected_dict = {'port': 80, 'url': 'fuck', 'method': 'POST'}
        real_dict = json.loads(str(service_instance))
        self.assertDictEqual(expected_dict, real_dict)

    def test_service_lib_has_instance(self):
        self.assertTrue(self.service_lib.has_service('sync'))
        self.assertTrue(self.service_lib.has_service('async'))
        self.assertFalse(self.service_lib.has_service('fuck'))

    def test_service_lib_get_instance(self):
        self.assertEqual(self.service_lib.get_service_instance('sync').port,
                         1000)
