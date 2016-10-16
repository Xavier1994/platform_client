Platform Client is a tool for tansfer http request to function call and provide some convinient wrappers


.. _installation:

Installation
============

Install, upgrade and uninstall platform_client with these commands::

    $ cd platform_client
    $ python setup.py install

Dependencies
============

The Platform-Client distribution is supported and tested on Python 2.7, 3.3, 3.4


Main dependency is:

- Requests: HTTP library for human beings (http://docs.python-requests.org/)

Additional dependencies are:

- Sphinx: Tool to create and manage the documentation (http://sphinx-doc.org/)
- Nose: to auto-discover tests (http://nose.readthedocs.org/en/latest/)
- Mock: to mock tests (https://pypi.python.org/pypi/mock)


Documentation
=============

Not Ready

Examples
========

Here's a basic example (for more see the examples directory)::

    $ python

    >>> from platform_client import PlatformClient
    >>> client = PlatformClient()
    >>> result = client.sync_import_image(repository_id = 1, picture_image_content_base64 = 'xxx')

See more examples in example folder

Testing
=======

Make sure you have tox by running the following::

    $ cd platform_client
    $ tox

Development
===========

All development is done on Github_. Use Issues_ to report
problems or submit contributions.

.. _Github: https://github.com/xavier/Platform_client/


TODO
====

- document, add comment to code for using Sphinx to generating doc


Source code
===========

The source code is currently available on Github: https://github.com/xavier/platform_client
