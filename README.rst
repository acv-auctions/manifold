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
    THRIFT = {
        'FILE': os.path.join(BASE_DIR, 'notification_service.thrift'),
        'SERVICE': 'NotificationService'
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
       THRIFT = {
           # Path to Thrift file, either absolute or relative
           'FILE': os.path.join(BASE_DIR, 'path/to/service.thrift'),

           # Thrift service defined in file to serve
           'SERVICE': 'MyServiceName'
       }

3. Run the server. You can either use the ``manage.py`` command:

   .. code:: bash

       python manage.py runrpcserver

   or you can use ``gunicorn_thrift`` to serve it in production as a
   worker pool.

   .. code:: bash

       gunicorn_thrift manifold.server.rpc:app -b 0.0.0.0:9090

Usage Guide
-----------

Below describes the basic usages of Manifold.

Handling RPC Calls
~~~~~~~~~~~~~~~~~~

Mapping and handling Thrift RPC functions works very similar to a Python
Flask application. We create a **Service Handler**, which handles
incoming Thrift functions and serves them with Python functions. The
Service Handler's method ``map_function`` actual performs the mapping.

.. code:: python

    from manifold.handler import create_handler

    # Create an RPC Service Handler to serve routes
    handler = create_handler()

    # Map the Thrift function 'schedule' to this function
    @handler.map_function('schedule')
    def schedule_job(job):
        """Schedule a service job to run
        """
        schedule_job_task(job)
        return True

Thrift File as Python Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Django project, it will most likely be necessary to serialize and
de-serialize Thrift structs. Manifold will automatically convert any
passed in arguments to your mapped functions as Python classes. For
example, let's say we have ``Status`` defined in our Thrift file, as we
do below.

.. code:: thrift

    struct Status {
        1: i16 code = 200,
        2: string response
    }

Using ``thrift_module``
***********************

We can then use ``Status`` in our code by importing the
``thrift_module`` module from ``manifold.file``, which contains all of
our structs and services we defined as Python classes. You can simply 
import or create instances directly through this module. An example using
the ``Status`` struct is shown below.

.. code:: python

    from manifold.file import new

    def perform_task(task):
      """Performs a task and returns a status
      :params:  Thrift struct Task instance
      :returns: Thrift struct Status instance
      """
      ret_value = perform_task(task)

      # Return a Thrift defined struct
      return thrift_module.Status(code=200, response=ret_value)
      
Using ``new`` shortcut
**********************

``thrift_module`` is good if you need low-level Thrift values, such as enums. 
If you want a quicker shortcut to create Thrift objects, we can use the ``new`` 
function from ``manifold.file``, which is a shortcut for ``thrift_module``.
``new`` takes in the desired instance type as a string, followed by any 
arguments (``*args``) and keyword arguments (``**kwargs``).
An example using the ``Status`` struct is shown below.

.. code:: python

    from manifold.file import new

    def perform_task(task):
      """Performs a task and returns a status
      :params:  Thrift struct Task instance
      :returns: Thrift struct Status instance
      """
      ret_value = perform_task(task)

      # Return a Thrift defined struct
      return new('Status', code=200, response=ret_value)

RPC Server
~~~~~~~~~~

The RPC Service will be responsible for listening and collecting
incoming RPC requests. It will validate these requests, and route them
to a RabbitMQ instance for them to be consumed. The service is
stateless, and can be scaled horizontally as much as desired.

It can be run with the following command:

.. code:: bash

    gunicorn_thrift manifold.rpc:app -b 0.0.0.0:9090

which then serves a RPC server on 0.0.0.0:9090. The configuration of
``gunicorn_thrift`` follows many of ``gunicorn``'s configs.

Validating Thrift Structs & Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validating Thrift structs and calls is made easy with Django and
Manifold. Simply create a subclass of
``manifold.validators.ThriftValidator`` that mirrors the attributes of
your Thrift struct. You can then validate any Thrift objects by
instantiating the Form with the Thrift object as an argument. An example
is shown below.

Our thrift declaration would be:

.. code:: thrift

    struct JobTemplate {
        1: list<i16> some_values,
        2: optional string other_value
    }

We would then have a ``Form`` defined somewhere:

.. code:: python

    from manifold.validators import ThriftValidator, ListField, StringField

    class JobTemplateValidator(ThriftValidator):

        # `some_values` must be int types, and the list must contain at least 1 item
        some_values = ListField(min_length=1, list_type=int)
        
        other_value = StringField(required=False, max_length=128)

and then we can use this in our code to provide a full Request -->
Response function like so:

.. code:: python

    from manifold.handler import create_handler
    from validators import JobTemplateValidator

    # Create an RPC Service Handler to serve routes
    handler = create_handler()

    # Map the Thrift function 'schedule' to this function
    @handler.map_function('schedule')
    def schedule_job(job):
        """Schedule a service job to run
        """
        validator = JobTemplateValidator(job)
        if not validator.is_valid():
            raise thrift_module.JobException(error='Invalid Job specified!')
        return True

Notice how we call ``is_valid()`` on our validator. Its very similar to
`Django Forms <https://docs.djangoproject.com/en/2.0/topics/forms/>`__,
because the validators actually are subclasses of ``django.forms``.

Also, notice how if ``job`` is not valid, we ``raise`` a
``thrift_module.JobException``. Manifold will catch any Thrift defined
exceptions and will return them as a response for the calling client to
handle. So for the example, we would have a ``JobException`` defined in
our Thrift interface like so:

.. code:: thrift

    // Exceptions are very similar to structs in Thrift.
    exception JobException {
        1: string error
    }

    struct Job {
        // Some definition...
    }

    // A simple JobService to contain our `schedule` function
    service JobService {

        // We define our function to take in a job, and return a boolean OR
        // throw a JobException that will be handled by the caller
        bool schedule(1: Job job) throws (1: JobException jobException),
    }

Manifold will return raised Thrift exceptions to the caller, but will
locally raise any uncaught Python, non-Thrift defined exceptions. So for
example, Manifold will safely catch the ``JobException`` below and
return it to the caller, but it will fail at the unhandled and
inevitable ``KeyError``.

.. code:: python

    from manifold.handler import create_handler
    from validators import JobTemplateValidator

    # Create an RPC Service Handler to serve routes
    handler = create_handler()

    # Map the Thrift function 'schedule' to this function
    @handler.map_function('schedule')
    def schedule_job(job):
        """Schedule a service job to run
        """
        # An invalid job will get the Thrift defined expection returned
        # to the calling program, but the function will end safely.
        validator = JobTemplateValidator(job)
        if not validator.is_valid():
            raise thrift_module.JobException(error='Invalid Job specified!')
            
        job_dict = job_to_dict(job)  # Some code to turn a Job into Python dictionary
        
        # The following will raise a KeyError if the key does not exist, and the caller
        # will be notified that they lost contact with the RPC server as the Python
        # thread will fail.
        return job_dict['non-existent-key']

Contributing Guide
------------------

This project is developed and maintained by `ACV
Auctions <https://www.acvauctions.com>`__. We are always open to outside
contributers helping to making Manifold better. To contribute, please
**fork** this repository, make your changes, and create a **Pull
Request** to merge your forked branch into the main master branch.

License
-------

Manifold is `BSD
Licensed <https://github.com/acv-auctions/manifold/blob/master/LICENSE>`__
