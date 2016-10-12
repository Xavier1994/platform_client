#!/usr/bin/env python
# -*- coding: utf-8 -*-

from platform_client import PlatformClient


# 装饰器本质上侵入了函数定义时的闭包,在函数定义时携带的作用域中
# 定义了与ServiceLib中的service同名的一些方法调用,只在函数调用过
# 程中起作用,函数调用结束之后就会从作用域中删除,做到不留痕迹

# 假设一个使用场景,我在本机上起了一个Car Platform,又在本机上需要
# 调用这个Car Platform的服务,那么有多方便呢,你只要在你的函数上加
# 一句@PlatformClient(), 然后就能用相应的函数调用这些服务了,我已
# 经想不到比这个更方便的了, 你什么都不用知道,只要调用方法就可以了
@PlatformClient()
def test():
    r = sync_import_image(repository_id=9999,
                          picture_base64_content='xxx')
    print(r.json())

if __name__ == '__main__':
    test()
