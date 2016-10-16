#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from platform_client import PlatformClient, ServiceInstance, ServiceLib


def main():
    service = ServiceInstance(url='/shit',
                              port=80,
                              access_method='POST')
    service_lib = ServiceLib({'shit': service})
    with PlatformClient(service_lib=service_lib, auth=None) as cli:
        # in fact, there just send a http request
        # method: POST
        # url: http://$host:80/shit
        # header: None, can specify header with __header={'Content-Type':'application/json'}
        # param: None, can sepecify params with __param={'shit':'fuck'}
        # body: {'p1':'shit', 'p2':'fuck'}
        result = cli.shit(p1='shit', p2='fuck')
        print(result.content)
        return 0

if __name__ == '__main__':
    sys.exit(main())
