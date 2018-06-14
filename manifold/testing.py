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
import json

from django.test import Client as DjangoClient

from manifold.file import load_module
from manifold.handler import handler


class RpcClient:
    pass


class HttpClient(DjangoClient):

    def send(self, route, data=None):
        if not route.startswith('/'):
            raise ValueError('RPC route must start with "/".')

        if data:
            data = json.dumps(data)

        return self.post(route, data=data, content_type='application/json')


def setup_test_env(settings_key='default'):
    """Allows easier integration testing by creating RPC and HTTP clients

    :param settings_key: Desired server to use
    :return: Tuple of RPC client, HTTP client, and thrift module
    """
    client = _create_test_client()
    return client, HttpClient(), load_module(settings_key)


def _create_test_client():
    ignored = ['configured', '_ServiceHandler__mapped_names']

    client = RpcClient()
    for attribute, value in vars(handler).items():
        setattr(client, attribute, value)

    for key in ignored:
        delattr(client, key)
    return client
