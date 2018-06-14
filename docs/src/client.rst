.. currentmodule:: manifold.rpc

.. _rpc_client:

RPC Client
----------

While Manifold is primarily designed to be a server-side application, it can also be used client-side to allow
Python applications to make RPC connections and function calls.

``make_client`` Function
========================

The ``make_client`` function will return a RPC client interface to easily call RPC functions with.

.. autofunction:: make_client

This function creates a client instance from the ``MANIFOLD`` settings defined by ``key`` parameter. The client
has methods matching the RPC functions, that take in :ref:`Thrift instances<conversion_to_python>`, and will return
the correct types back.

For example, if we have the following Thrift service defined in ``thrift/pingPong.thrift``:

::

    service PingPongService {
        string ping(1: i16 repeated),
    }

Then we would define that in our Django settings for our client as:

.. code-block:: python
   :linenos:

   MANIFOLD = [
       'ping_pong': {
           'file': 'thrift/pingPong.thrift',
           'service': 'PingPongService',
           'host': '127.0.0.1',
           'port': 5590
       }
   ]

*Notice how we added `host` and `port`, compared to the server configuration! This is needed by clients so they
know where to connect!*

Let's assume that when we call ``ping``, it will return the string ``"pong"`` repeated ``repeated`` times. We
could then call and assert our function response in the following manner.

.. code-block:: python
   :linenos:

   from manifold.rpc import make_client

   client = make_client(key='ping_pong')

   response = client.ping(2)

   assert response == 'pongpong'

This code creates the client, sends the call with the given arguments, and asserts the response given back.
Arguments and responses have to and will match their Thrift equivalents.


