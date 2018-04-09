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
from unittest import mock

from django.test import TestCase
from thriftpy.thrift import TProcessor

from manifold import rpc
from manifold.file import load_service


class RPCTestSuite(TestCase):

    maxDiff = None

    def test_get_rpc_application(self):
        app = rpc.get_rpc_application()
        rpc.handler.configured = None
        self.assertEqual(type(app), TProcessor)

    def test_make_server(self):
        self.assertIsNotNone(rpc.make_server())

    @mock.patch('manifold.rpc.thrift_client', autospec=True)
    def test_make_client(self, mocked_client):
        client = rpc.make_client()
        self.assertIsNotNone(client)

        mocked_client.assert_called_with(
            load_service(),
            host='127.0.0.1',
            port=9090
        )
