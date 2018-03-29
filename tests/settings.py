"""
Copyright 2018 ACV Auctions

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# pylint: disable=W0401,W0614
import sys

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

# HTTP Settings
WSGI_APPLICATION = 'manifold.http.application'
ROOT_URLCONF = 'manifold.http'

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

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s]'
                      ' %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True
        },
    }
}
