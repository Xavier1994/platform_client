"""
Python client for Yitu Platform
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .service_helper import ServiceHelper


_default_service_json = {

    # Service name and json config
    'sync_import_image': {'port': 9110,
                          'method': 'POST',
                          'url': '/car/picture/synchronized'},
    'async_import_image': {'port': 9110,
                           'method': 'POST',
                           'url': '/car/picture'},
    'create_repository': {'port': 9900,
                          'method': 'POST',
                          'url': '/car/v1/framework/car_image/repository'},
    'update_repository': {'port': 9900,
                          'method': 'PUT',
                          'url': '/car/v1/framework/car_image/repository'},
    'get_repository': {'port': 9900,
                       'method': 'GET',
                       'url': '/car/v1/framework/car_image/repository'},
    'delete_repository': {'port': 9900,
                          'method': 'DELETE',
                          'url': '/car/v1/framework/car_image/repository'},
    'get_camera': {'port': 9900,
                   'method': 'GET',
                   'url': '/car/v1/framework/car_video/camera'},
    'create_camera': {'port': 9900,
                      'method': 'POST',
                      'url': '/car/v1/framework/car_video/camera'},
    'update_camera': {'port': 9900,
                      'method': 'PUT',
                      'url': '/car/v1/framework/car_video/camera'},
    'delete_camera': {'port': 9900,
                      'method': 'DELETE',
                      'url': '/car/v1/framework/car_video/camera'},
    'get_picture': {'port': 7300,
                    'url': '/storage/v1/image',
                    'method': 'GET'},
    'query': {'port': 9210,
              'url': '/car/query',
              'method': 'POST'},
    'retrievel': {'port': 9210,
                  'url': '/car/retrieval',
                  'method': 'POST'},
    'update': {'port': 9210,
               'url': '/car/update',
               'method': 'POST'}
}

default_service_lib = \
    ServiceHelper.load_service_lib_from_json(_default_service_json)
