from unittest import mock

from django.apps import apps
from django.test import TestCase

from django_thrift.apps import DjangoThriftConfig
from django_thrift.handler import ServiceHandler


class AppTestSuite(TestCase):

    def test_apps(self):
        self.assertEqual(DjangoThriftConfig.name, 'django_thrift')
        self.assertEqual(apps.get_app_config('django_thrift').name, 'django_thrift')


class ServiceHandlerTests(TestCase):

    def test_service_handler_mapping(self):
        handler = ServiceHandler()

        @handler.map_function('test_call')
        def test_function():
            return "Hello World"

        self.assertEqual(handler.test_call(), "Hello World")

    def test_service_handler_duplicate_name(self):
        handler = ServiceHandler()

        @handler.map_function('test_call')
        def test_function():
            return "Hello World"  # pragma: no cover

        with self.assertRaises(NameError):
            @handler.map_function('test_call')
            def another_function():
                return "Oops!"  # pragma: no cover

    @mock.patch('django_thrift.handler.agent')
    def test_raise_new_relic_warning(self, mocked_agent):
        mocked_agent.set_transaction_name.side_effect = Exception(
            'Could not set New Relic Transaction'
        )

        handler = ServiceHandler()

        @handler.map_function('test_call')
        def test_function():
            return "Hello World"

        self.assertEqual(handler.test_call(), "Hello World")

