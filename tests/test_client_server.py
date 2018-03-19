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
from threading import Thread
from time import sleep

from django.test import TestCase

from manifold.rpc import make_server, make_client


class FileTestSuite(TestCase):

    SLEEP = 2

    server = None

    def run_test_server(self):
        if not self.server:
            server = make_server()
            self.assertIsNotNone(server)
            server.serve()

    def test_valid_client_server_interaction(self):
        # Start server
        Thread(target=self.run_test_server).start()
        sleep(self.SLEEP)

        # Test the client
        client = make_client()

        self.assertTrue(client.pingPong(5))

    def test_false_client_server_interaction(self):
        # Start server
        Thread(target=self.run_test_server).start()
        sleep(self.SLEEP)

        # Test the client
        client = make_client()

        self.assertFalse(client.pingPong(4))
