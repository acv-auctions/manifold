.. _quickstart:

Quickstart Guide
================

Follow the steps below to get started with :code:`django-manifold`.

Create Thrift File
******************

Either create or use an existing Thrift file for Manifold to serve and connect with. For example, we can use the
one below, which will be located in our project root at :code:`service.thrift`

::

    struct Task {
        1: i32 user_id,
        2: string status
    }

    service ExampleService {
        bool schedule(1: Task task),
    }

Installation
************

You can install :code:`django-manifold` via :code:`pip`. This will also install its dependencies.

.. code-block:: python

   pip install django-manifold


Configure Settings
******************

Once installed, add :code:`manifold` to your Django settings's :code:`INSTALLED_APPS`. This will allow you to use
Manifold's features.

.. code-block:: python

   INSTALLED_APPS = [
       # ... other apps
       'manifold',
       # ... other apps
   ]

Once added, we can then define Manifold's settings by creating the :code:`MANIFOLD` dictionary. Here you define where
Manifold can find your Thrift services, their files, and how to identify them. It takes a **key** that references that
specific configuration, and settings inside that key's dictionary.

Note that you can call these keys whatever you want, its how you reference them. If you plan on using Manifold as an
RPC server, then you currently *must* have a :code:`default` key, as this is what the server uses as its
configuration.

.. code-block:: python
   :linenos:

   MANIFOLD = [
       'default': {
           'file': os.path.join(BASE_DIR, 'service.thrift'),
           'service': 'ExampleService'
       }
   ]

Define RPC Routes
*****************

Next, we will design a route for Manifold to use to handle incoming function requests to :code:`schedule`. We will
put this in any project app we want in :code:`views.py`.

*Note that currently all RPC routes must be defined in :code:`views.py` for an app*

.. code-block:: python
   :linenos:

   from manifold.handler import handler


   @handler.map_function('schedule')
   def handle_schedule(task):
       print(task)
       # Do whatever you need to
       # ...
       return True

Run RPC Server Locally
**********************

To run the server locally, you can use the following Django management command.

.. code-block:: bash

   python manage.py runrpcserver

Run RPC Server in Production
****************************

To run the RPC server in production, we can use `Gunicorn Thrift <https://github.com/eleme/gunicorn_thrift>`__.
This is installed as a dependency, so you don't have to worry about managing it. :code:`gunicorn_thrift` is a
wrapper around normal WSGI Gunicorn, so if you've used the latter, you should be pretty familiar with the former.

Similar to Django's :code:`wsgi.py`, we will need to create a file :code:`rpc.py` in the project root app. It should
contain the following code, let's say it is in :code:`project/wsgi.py`.

.. code-block:: python
   :linenos:

   import os

   from manifold.rpc import get_rpc_application

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

An example command you can run is shown below:

.. code-block:: bash

   gunicorn_thrift project.rpc:app -b 0.0.0.0:9090


Run HTTP Server Locally
***********************

If you want to test with the HTTP server that wraps around the RPC calls, you will need to add a bit more settings.
We will have to set/change the :code:`WSGI_APPLICATION` and :code:`ROOT_URLCONF` settings, to the values below.

.. code-block:: python

   WSGI_APPLICATION = 'manifold.http.application'
   ROOT_URLCONF = 'manifold.http'

You will then be able to test the HTTP server as you normally would with the :code:`runserver` command.

.. code-block:: bash

   python manage.py runserver

This should be enough to get your project rolling with :code:`django-manifold`. For more configuration, usage, and
setup, please read the rest of the documentation.
