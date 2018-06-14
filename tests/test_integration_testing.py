import types

from django.test import TestCase
from manifold.testing import setup_test_env, HttpClient, RpcClient


class TestingUtilsTestSuite(TestCase):

    def test_env_creation(self):
        rpc, http, module = setup_test_env()
        self.assertIsNotNone(rpc, RpcClient)
        self.assertIsInstance(http, HttpClient)
        self.assertIsInstance(module, types.ModuleType)

    def test_rpc_client_call(self):
        rpc, _, _ = setup_test_env()
        self.assertTrue(rpc.pingPong(5))

    def test_http_client_call_invalid(self):
        _, http, _ = setup_test_env()
        response = http.send('/pingPong').json()
        self.assertEqual(response['response'], 'error')

    def test_http_client_call_invalid_route(self):
        _, http, _ = setup_test_env()
        with self.assertRaises(ValueError):
            http.send('pingPong', {'val': 5})

    def test_http_client_call_valid(self):
        _, http, _ = setup_test_env()

        response = http.send('/pingPong', {'val': 5}).json()
        self.assertTrue(response['return'])
