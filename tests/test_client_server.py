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
