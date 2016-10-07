from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class PlatformClientError(Exception):
    """Raised when an error occurs in the request."""
    def __init__(self, content, code=None):
        if isinstance(content, type(b'')):
            content = content.decode('UTF-8', 'replace')

        if code is not None:
            message = "%s: %s" % (code, content)
        else:
            message = content

        super(PlatformClientError, self).__init__(
            message
        )
        self.content = content
        self.code = code


class PlatformServerError(Exception):
    """Raised when a server error occurs."""
    def __init__(self, content):
        super(PlatformServerError, self).__init__(content)


class PlatformNotLoginError(Exception):
    """Raised when the user is not login."""
    def __init__(self, user):
        content = 'current user: ' + user + ' not login'
        super(PlatformNotLoginError, self).__init__(content)


class PlatformInvalidAccessMethodError(Exception):
    """Raised when url instance's method is invalid"""
    def __init__(self, method):
        content = 'Not Support Method: ' + str(method)
        super(PlatformInvalidAccessMethodError, self).__init__(content)


class PlatformInvalidUrlError(Exception):
    def __init__(self, url):
        content = 'Not Support Url: ' + url
        super(PlatformInvalidUrlError, self).__init__(content)


class PlatformConstantSetError(Exception):
    def __init__(self, url):
        super(PlatformConstantSetError, self).__init__(content)


class PlatformAuthFailedError(Exception):
    def __init__(self, content):
        super(PlatformAuthFailedError, self).__init__(content)
