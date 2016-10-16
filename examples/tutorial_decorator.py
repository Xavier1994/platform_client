#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from platform_client import PlatformClient


@PlatformClient()
def test():
    """
    in fact, here just insert these methods into the function test's
    closure and make test function can call these services in fu
    body
    """
    r = sync_import_image(repository_id=9999,
                          picture_base64_content='xxx')
    print(r.json())

if __name__ == '__main__':
    sys.exit(test())
