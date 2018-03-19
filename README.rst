Manifold: Django Thrift RPC Implementation
==========================================

Manifold is a `Django <https://www.djangoproject.com>`__ application
designed by `ACV Auctions <https://acvauctions.com>`__ that allows for
easy creation and serving of an RPC server through a WSGI interface
using `Gunicorn Thrift <https://github.com/eleme/gunicorn_thrift>`__.
Manifold uses `Apache Thrift <https://thrift.apache.org>`__ to
standardize message transmission.

It allows the Django project to define the Thrift file location and
service to be defined in the settings file, which is shown below.

.. code:: python

    # Thrift Configurations
    MANIFOLD = {
        'default': {
            # Path to Thrift file, either absolute or relative
            'file': os.path.join(BASE_DIR, 'path/to/service.thrift'),
            'service': 'MyServiceName'
        }
    }

With these settings, you can do a few things. Define Python functions to
handle RPC calls, load the Thrift *in memory* as a Python module, and
serve an RPC WSGI server in both development and production.

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

Quickstart
----------

1. Add ``manifold`` to your ``INSTALLED_APPS`` setting like this:

   .. code:: python

       INSTALLED_APPS = [
           # ...
           'manifold',
       ]

2. Define your Thrift configuration like this:

   .. code:: python

       # Thrift Configurations
       MANIFOLD = {
           'default': {
               # Path to Thrift file, either absolute or relative
               'file': os.path.join(BASE_DIR, 'path/to/service.thrift'),
               'service': 'MyServiceName'
           }
       }

3. Run the server. You can either use the ``manage.py`` command:

   .. code:: bash

       python manage.py runrpcserver

   or you can use ``gunicorn_thrift`` to serve it in production as a
   worker pool.

   .. code:: bash

       gunicorn_thrift manifold.rpc:app -b 0.0.0.0:9090

Usage Guide
-----------

View the `wiki <https://github.com/acv-auctions/manifold/wiki>`__ for usage guides.


Contributing Guide
------------------

This project is developed and maintained by `ACV
Auctions <https://www.acvauctions.com>`__. We are always open to outside
contributers helping to making Manifold better. To contribute, please
**fork** this repository, make your changes, and create a **Pull
Request** to merge your forked branch into the main master branch.

License
-------

Manifold is `Apache 2.0 Licensed <https://github.com/acv-auctions/manifold/blob/master/LICENSE>`__
