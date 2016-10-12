# -*- coding: utf-8 -*-

#  ____  _       _    __                         ____ _ _            _
# |  _ \| | __ _| |_ / _| ___  _ __ _ __ ___    / ___| (_) ___ _ __ | |_
# | |_) | |/ _` | __| |_ / _ \| '__| '_ ` _ \  | |   | | |/ _ \ '_ \| __|
# |  __/| | (_| | |_|  _| (_) | |  | | | | | | | |___| | |  __/ | | | |_
# |_|   |_|\__,_|\__|_|  \___/|_|  |_| |_| |_|  \____|_|_|\___|_| |_|\__|

"""
Platform Client -> Transfer Platform Http Service To Specific funtion call
~~~~~~~~~~~~~~~~~~~~

Formal usage:

    >>> from platform_client import PlatformClient
    >>> cli = PlatformClient()
    >>> r = cli.sync_import_image(repository_id=9999, picture_image_content_base64='xxx')
    >>> r.status_code
    200

Context usage:

    >>> from platform_client import PlatformClient
    >> with PlatformClient() as cli:
        r = cli.sync_import_image(repository_id=9999, picture_image_content_base64='xxx')
        print r.status_code
    200

Decorator usage:

    >>> from Platform import PlatformClient
    >>> @PlatformClient()
        def test():
            r = sync_import_image(repository_id=9999, picture_image_content_base64='xxx')
            print r.status_code
    >>> test()
    200

See more in examples

:copyright: (c) 2016 by Wei Xie.
:license: Apache 2.0, see LICENSE for more details.
"""

__title__ = 'paltform_client'
__version__ = '1.0.0'
__author__ = 'Wei Xie'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Wei Xie'

from .client import PlatformClient
from .service_lib import ServiceInstance, ServiceLib
from .service_helper import ServiceHelper


__all__ = [
    'PlatformClient',
    'PlatformAuth',
    'ServiceInstance',
    'ServiceLib',
    'ServiceHelper'
]
