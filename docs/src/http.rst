Using HTTP Wrapping Server
==========================

Manifold contains built in support to wrap the RPC configuration around a WSGI HTTP server, instead of the RPC
server. This allows languages and frameworks that don't communicate easily with Thrift or RPC to still interact with
the services using ``POST`` requests and JSON.

Setting Up the HTTP Server
**************************

To set up a normal Django application with Manifold, view the :ref:`Quickstart Guide <quickstart>`.

Once created, we can make sure to add the followings settings to our ``DJANGO_SETTINGS_MODULE``.

.. code-block:: python

   WSGI_APPLICATION = 'manifold.http.application'
   ROOT_URLCONF = 'manifold.http'

The ``WSGI_APPLICATION`` overwrites what Django originally has, which falls somewhere in your project root.
``manifold.http.application`` is automatically created to have the RPC routes defined as URLs, as well as providing
wrappers to convert JSON to Thrift structs, and vis versa. The ``ROOT_URLCONF`` let's Django use our RPC functions
mapped to URLs.

Running the HTTP Server
***********************

Once configured, you can run the command below, just as you would with any Django project:

.. code-block:: bash

   python manage.py runrpcserver

RPC Functions to URL Routes
***************************

Obviously via HTTP we can't just call an RPC function anymore, so to interact with the server, we will have to use
HTTP routes. Manifold's HTTP server takes every RPC function that is wrapped using ``handler.map_function`` and
converts it into a REST API endpoint with the same name.

Note, it doesn't use the function name, it uses the string passed to :code:`handler.map_function` that is the name of
the RPC call defined in Thrift. For example:

.. code-block:: python
   :linenos:

   from manifold.handler import handler


   @handler.map_function('schedule')
   def handle_schedule(task):
       print(task)
       # Do whatever you need to
       # ...
       return True

would be accessible at ``/schedule`` from whatever location the server is being hosted on.

.. _sending_data:

Sending Data to the HTTP Server
*******************************

Let's say we have the following Thrift structure defined in our Manifold configuration:

::

    struct Task {
        1: i32 user_id,
        2: string status
    }

    service ExampleService {
        bool schedule(1: Task task),
    }

We can then call this ``schedule`` RPC function by running the HTTP server and sending a ``POST`` request to
``/schedule``. We will attach JSON to the request to represent the task, so don't forget to set the ``Content-Type``
heading to ``application/json``!!

To represent the arguments, we will build a JSON object that reflects the ``Task`` structure. If you don't need a field, or
it's optional, you can just exclude it. The top level keys in the JSON object must match the names of the Thrift function
arguments. To represent the above ``scheule`` function, we would have a JSON structure as follows:

.. code-block:: json

   {
       "task": {
           "user_id": 123,
           "status": "reset-password"
       }
   }

If we had a Thrift function that took in multiple arguments, such as and ``compute`` function shown below, we can
just have multiple top level keys.

::

    service CalculatorService {
        i64 compute(1: i32 argA, 2: i32 argB, 3: string operation),
    }

We would be able to call and get a response from the HTTP server by sending a request to ``/compute`` with the
following JSON data:

.. code-block:: json

   {
       "argA": 15,
       "argB": 30,
       "operation": "+"
   }

Note that if structs contain other structs, you just have to deserialize the children structs in a similar manner.


Responses from the HTTP Server
******************************

All responses will be returned with JSON. The JSON data will at least contain a ``"response"`` key, that is either
``"ok"`` or ``"error"``. There are three types of responses that will come from the server (minus a 500 error).

Parsing Error
-------------

A Parsing Error occurs when one way or another, the HTTP server can't convert the given JSON data into the
correct format, or something goes wrong before the actual Thrift handler is called. These are usually due to
malformed requests. The response from these have the following structure:

.. code-block:: json

   {
       "response": "error",
       "error": "Expected 'val' key."
   }

To fix these, make sure that your JSON data being sent into the server is correct. See `Sending Data to the HTTP Server`_.

Thrift-Defined Exception
------------------------

A Thrift Exception means a Thrift-defined exception was raised during the runtime of the RPC handling function. This is
usually not a data parsing issue, but identifying an issue with the data represented. With these errors, mirrored RPC
calls would likely also fail, so check your logic and conditions.

If we had an exception defined in our Thrift file as such:

::

   exception ExampleException {
       1: string error,
   }

Then the response from these requests when raised would have the following structure:

.. code-block:: json

   {
       "response": "error",
       "exceptionType": "ExampleException",
       "exception": {
           "error": "Something went wrong!"
       }
   }

The exception type name is given, along with a JSON representation of the exception.

Successful Responses
--------------------

Finally! The response you hope for and expect! A successful response always come with a ``"response"`` key that is
``"ok"``. It will also have a ``"return"`` key which will contain a JSON structure of the Thrift output, in the correct
format denoted by the Thrift file. This works for basic types, structs, and complex structs inside of others. The
serialized format will follow the same structure as described in :ref:`Sending Data to the HTTP Server <sending_data>`
