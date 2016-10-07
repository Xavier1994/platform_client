# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import unitetst2 as unittest
except ImportError:
    import unittest

from platform_client.service_helper import ServiceHelper


class TestServceHelper(unittest.TestCase):

    def setUp(self):
        self.json_content = {'sync_import_image': {
                                'port': 8000,
                                'url': '/haha',
                                'method': 'GET'
                               }
                            }

    def test_load_service_lib_from_json(self):
        service_lib = ServiceHelper.load_service_lib_from_json(self.
                                                               json_content)

        self.assertTrue(service_lib.has_service('sync_import_image'))
        self.assertEqual(8000,
                         service_lib.get_service_instance('sync_import_image').
                         port)
