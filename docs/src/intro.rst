Django Manifold Introduction
============================

Manifold is a `Django <https://www.djangoproject.com>`__ application
designed by `ACV Auctions <https://acvauctions.com>`__ that allows for
easy creation and serving of an RPC server through a WSGI interface
using `Gunicorn Thrift <https://github.com/eleme/gunicorn_thrift>`__.
Manifold uses `Apache Thrift <https://thrift.apache.org>`__ to
standardize message transmission.

Manifold comes with a plethora of features:

* Local and production level RPC server applications / commands.
* RPC Server application to make it easier to pool RPC servers in a Django-esque way.
* Service Handler that decorates Python functions to allow them to handle RPC function requests and responses.
* In-memory generation of Thrift file, giving access to Thrift structs, services, and values as a Python module, without the need of CLI generation
* Validation of Thrift structs, even when contained within eachother.
* Configuration to serve Django's WSGI application as a JSON wrapper around the RPC interface, allowing non-Thrift access.
* Easy exception handling back to caller for Thrift defined Exceptions.

In the future, we hope Manifold will expand to include `gRPC <https://grpc.io/>`__.

If you have any requests, please visit `the GitHub issues <https://github.com/acv-auctions/manifold/issues>`__.


