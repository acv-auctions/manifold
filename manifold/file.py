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
from django.conf import settings
import thriftpy

_cached_modules = {}


def load_module(key='default'):
    """Loads a Python module to use Thrift defined structures and types
    :param key: The MANIFOLD settings key to use for configuration loading
    :return: A Python module that has the Thrift types/structs defined within it
    """
    thrift = settings.MANIFOLD[key]
    if key in _cached_modules:
        return _cached_modules[key]
    module = thriftpy.load(
        thrift['file'],
        module_name=thrift['file'].replace('.', '_')
    )
    _cached_modules[key] = module
    return module


def load_service(key='default'):
    module = load_module(key)
    return getattr(module, settings.MANIFOLD[key]['service'])
