# pylint: disable=W0401,W0614
from django.conf.global_settings import *

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
SECRET_KEY = 'not very secret in tests'
INSTALLED_APPS = [
    'manifold',
    'tests.example_app'
]
MANIFOLD = {
    'default': {
        'file': 'tests/example.thrift',
        'service': 'ExampleService'
    },
    'non-default': {
        'file': 'tests/secondary.thrift',
        'service': 'DummyService',
        'host': '127.0.0.1',
        'port': 9090
    }
}
