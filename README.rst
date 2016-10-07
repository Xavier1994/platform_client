

Platform-Client is a client for interacting with Platform(include car and face) Maintained by @phate (phate1994@gmail.com)

.. _readme-about:

InfluxDB is an open-source distributed time series database, find more about InfluxDB_ at http://influxdata.com/


.. _installation:

Installation
============

Install, upgrade and uninstall InfluxDB-Python with these commands::

    $ cd platform_client
    $ python setup.py install

Dependencies
============

The Platform-Client distribution is supported and tested on Python 2.7, 3.3, 3.4


Main dependency is:

- Requests: HTTP library for human beings (http://docs.python-requests.org/)

Additional dependencies are:

- pandas: for writing from and reading to DataFrames (http://pandas.pydata.org/)
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

    >>> client = PlatformClient('localhost', 7500, 'system', 'YituTect837')

    >>> result = client.sync_import_image(repository_id = 1, picture_image_content_base64 = 'xxx') 

    >>> print("Result: {0}".format(result))


Testing
=======

Make sure you have tox by running the following::

    $ cd platform_client
    $ nosetests -v

Development
===========

All development is done on Github_. Use Issues_ to report
problems or submit contributions.

.. _Github: https://github.com/xavier/Platform_client/


TODO
====

So many things


Source code
===========

The source code is currently available on Github: https://github.com/xavier/platform_client
