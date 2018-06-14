.. currentmodule:: manifold.testing

Testing
-------

Don't let testing be difficult! With Django Manifold, you can easily run integration tests to ensure
everything is sound and working. Manifold comes with a test RPC client and a test HTTP client that
you can make real requests to during tests.

Setting Up Test Environment
+++++++++++++++++++++++++++

Use the ``setup_test_env`` function to create any necessary clients and thrift modules needed for
integration testing.

.. autofunction:: setup_test_env

You can use this function in your test cases in a similar fashion to the following. For using each
client, please refer to the sections below.

.. code-block:: python

   from django.test import TestCase
   from manifold.testing import setup_test_env

   class RPCCallTestSuite(TestCase):

       def setUp(self):
           rpc, http, thrift_module = setup_test_env('default')
           self.rpc_client = rpc
           self.http_client = http
           self.t_module = thrift_module

The examples below will assume the following Thrift interface, and the following Python handler for the call.

::

   service PingPongService {
       string ping(1: i16 repeated),
   }

And then the python code:

.. code-block:: python

   from manifold.handler import handler

   @handler.map_function('ping')
   def handle_ping(repeated):
       return 'ping' * repeated


Testing RPC Calls
+++++++++++++++++

Testing RPC calls uses the same interface as the normal :ref:`rpc_client`, except that the requests will
stay internal to the testing thread.

To test ``ping``, we could use the following test case.

.. code-block:: python

   from django.test import TestCase
   from manifold.testing import setup_test_env


   class PingCallTestCase(TestCase):

       def setUp(self):
           """Create the rpc and http client with the thrift module
           """
           rpc, http, thrift_module = setup_test_env('default')
           self.rpc_client = rpc
           self.http_client = http
           self.t_module = thrift_module

       def test_returns_correctly(self):
           # Call the handler with whatever args.
           # This is the same as calling it from
           # a legit client.
           response = self.rpc_client.ping(2)

           self.assertEqual('pingping', response)


Testing HTTP Wrapper Calls
++++++++++++++++++++++++++

Testing HTTP calls that wrap the HTTP server uses the same interface as the normal
Django Test client, except that it is subclassed as more extra features are added.
Most notably, the ``send`` method is added to shortcut the test client set up for
HTTP wrapped RPC requests.

To test ``ping`` via HTTP, we could use the following test case.

.. code-block:: python

   from django.test import TestCase
   from manifold.testing import setup_test_env


   class PingCallTestCase(TestCase):

       def setUp(self):
           """Create the rpc and http client with the thrift module
           """
           rpc, http, thrift_module = setup_test_env('default')
           self.rpc_client = rpc
           self.http_client = http
           self.t_module = thrift_module

       def test_returns_correctly(self):
           # Call the handler with whatever args.
           # This is the same as calling it from
           # a legit client.
           response = self.http_client.send(
               '/ping',    # First, the route, starting with `/`
               {'val': 5}  # The data dict to be included with the request
           )

           self.assertEqual('pingping', response)
