Manifold: Django Thrift RPC Implementation
==========================================

.. image:: https://travis-ci.org/acv-auctions/manifold.svg?branch=master

Manifold is a `Django <https://www.djangoproject.com>`__ application
designed by `ACV Auctions <https://acvauctions.com>`__ that allows for
easy creation and serving of an RPC server through a WSGI interface
using `Gunicorn Thrift <https://github.com/eleme/gunicorn_thrift>`__ and
`Thriftpy <https://github.com/eleme/thriftpy>`__.
Manifold uses `Apache Thrift <https://thrift.apache.org>`__ to
standardize message transmission.

It allows the Django project to define Thrift file locations and
services in the settings file. This then gives the power to define Python functions
to handle RPC calls, load the Thrift files *in memory* as a Python module,
serve an RPC WSGI server in both development and production, and serve a HTTP wrapper
around our RPC functions for frameworks and languages that don't have RPC support.

.. contents:: Table of Contents

Credits and Maintenance
-----------------------

Manifold is built using `Django <https://www.djangoproject.com>`__ and
`Thriftpy <https://github.com/eleme/thriftpy>`__, and is maintained by
`ACV Auctions <https://www.acvauctions.com>`__.

Thrift Guide
------------

For an introduction and in-depth description of Thrift, we recommend
following `Thrift: The Missing
Guide <https://diwakergupta.github.io/thrift-missing-guide/>`__.

Usage Guide
-----------

View the `documentation <http://django-manifold.readthedocs.io/en/latest>`__ for usage guides.


Contributing Guide
------------------

This project is developed and maintained by `ACV
Auctions <https://www.acvauctions.com>`__. We are always open to outside
contributers helping to making Manifold better. Please refer to
our `Contribution Guide <https://github.com/acv-auctions/manifold/blob/master/CONTRIBUTING.md>`__ to make a change.

License
-------

Manifold is `Apache 2.0 Licensed <https://github.com/acv-auctions/manifold/blob/master/LICENSE>`__
