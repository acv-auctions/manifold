import json

from django.test import TestCase, Client

from manifold import http


class HTTPTestSuite(TestCase):

    client = Client()

    def test_urlpatterns_length(self):
        self.assertEqual(len(http.urlpatterns), 5)

    def test_no_args_call(self):
        response = self.client.post('/pong', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"return": null, "response": "ok"}'
        )

    def test_no_args_provided_error(self):
        response = self.client.post('/pingPong')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"response": "error", "error": "Invalid Thrift request."}'
        )

    def test_args_call(self):
        response = self.client.post(
            '/pingPong',
            json.dumps({'val': 5}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"return": true, "response": "ok"}'
        )

        response = self.client.post(
            '/pingPong',
            json.dumps({'val': 3}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"return": false, "response": "ok"}'
        )

    def test_args_call_invalid_key(self):
        response = self.client.post(
            '/pingPong',
            json.dumps({'value': 5}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"response": "error", '
            b'"error": "\\"Expected \'val\' argument.\\""}'
        )

    def test_nested_struct_call(self):
        response = self.client.post(
            '/complex',
            json.dumps({
                'val': {
                    'some_string': 'Hello World',
                    'innerStruct': {'val': 123}
                }
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"return": {"some_string": "Hello World", '
            b'"innerStruct": {"val": 234}}, "response": "ok"}',
        )

    def test_multi_val_argument(self):
        response = self.client.post(
            '/multiVarArgument',
            json.dumps({
                'val1': 123,
                'val2': 321
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"return": false, "response": "ok"}',
        )

    def test_multi_val_argument_missing(self):
        response = self.client.post(
            '/multiVarArgument',
            json.dumps({
                'val1': 123,
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"response": "error", "error": "\\"Expected '
            b'\'val2\' argument.\\""}'
        )
