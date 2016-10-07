"""
Python client for Yitu Platform
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json

from .service_lib import ServiceInstance
from .service_lib import ServiceLib


class ServiceHelper(object):

    @staticmethod
    def load_service_lib_from_json(content):
        services = {}
        for item in content:
            services[item] = ServiceInstance(
                url=content[item].get('url'),
                port=content[item].get('port'),
                access_method=content[item].get('method')
            )

        return ServiceLib(services)

    @staticmethod
    def load_service_lib_from_file(file_path):
        with open(file_path, 'r') as f:
            content = json.load(f)
            return ServiceHelper.load_service_lib_from_json(content)
