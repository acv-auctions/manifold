# Change Log

All changes will be reflected here in reverse chronological order going down the document.

## Latest (Unreleased)

* No latest changes

## Version 1.3.1

Fixed requirements to not be as strict.

## Version 1.3

* Updated Makefile to have linting and testing be separate.
* Included `coverage` in test-suite
* Many more tests added to ensure good coverage (> 85)
* Travis CI added for testing
* Read The Docs cleaned up and deployed

## Version 1.2

* Added HTTP server wrapper around RPC ServiceHandler, allowing the service to be served using HTTP and JSON POSTs requests.
* `docs` directory added with all of the documentation.
* `runrpcserver` command updated to give more information and to run with autoreloader.
* Error messages for invalid validator fields give more concise and helpful information.
* Caches `load_module` modules.

## Version 1.1

* Updated `setup.py` to include checks and confirmations to ensure that deployment steps were followed
* Updated `setup.py` to include value pulling from `manifold.__init__`
* Changed `create_processor` to `get_rpc_application` to mimic Django's `get_wsgi_application`


## Version 1.0

Initial stable release.

* Includes support for multiple Manifold settings.
