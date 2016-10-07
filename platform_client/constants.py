# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .exceptions import PlatformConstantSetError


def constant(f):
    def fset(self, value):
        raise PlatformConstantSetError

    def fget(self):
        return f()
    return property(fget, fset)


class _Const(object):
    @constant
    def GET_METHOD():
        return 'GET'

    @constant
    def POST_METHOD():
        return 'POST'

    @constant
    def PUT_METHOD():
        return 'PUT'

    @constant
    def DELETE_METHOD():
        return 'DELETE'

    @constant
    def METHODS():
        return ['GET', 'POST', 'PUT', 'DELETE']

CONST = _Const()
