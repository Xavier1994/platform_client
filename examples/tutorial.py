#!/usr/bin/env python
# -*- coding: utf-8 -*-

from platform_client import PlatformClient, ServiceInstance, ServiceLib


def main():
    service = ServiceInstance(url='/shit',
                              port=80,
                              access_method='POST')
    service_lib = ServiceLib({'shit': service})
    with PlatformClient(service_lib=service_lib, auth=None) as cli:
        # 本质上,这里实际上是发送了一个http请求, 请求长这样
        # method: POST
        # url: http://$host:80/shit
        # header: None, 可以指定，比如传入__header={'Content-Type':'application/json'}
        # param: None, 可以制定,比如__param={'shit':'fuck'}
        # body: {'p1':'shit', 'p2':'fuck'}
        return cli.shit(p1='shit', p2='fuck')

if __name__ == '__main__':
    main()
