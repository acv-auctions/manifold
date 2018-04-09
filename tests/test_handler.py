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

from manifold.handler import ServiceHandler


# pylint: disable=W0612
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

    @mock.patch('manifold.handler.agent')
    def test_raise_new_relic_warning(self, mocked_agent):
        mocked_agent.set_transaction_name.side_effect = Exception(
            'Could not set New Relic Transaction'
        )

        handler = ServiceHandler()

        @handler.map_function('test_call')
        def test_function():
            return "Hello World"

        self.assertEqual(handler.test_call(), "Hello World")

    @mock.patch("builtins.print", autospec=True, side_effect=print)
    def test_print_out_mappings(self, mocked_print):

        handler = ServiceHandler()

        @handler.map_function('test_call')
        def test_function():
            return "Hello World"

        handler.print_current_mappings()
        args = mocked_print.call_args_list
        self.assertEqual(
            [mock.call('* test_call -- tests.test_handler.test_function',)],
            args
        )

    def test_get_mappings(self):
        handler = ServiceHandler()

        @handler.map_function('test_call')
        def test_function():
            return "Hello World"

        expected = {
            'test_call': test_function
        }

        mappings = handler.get_current_mappings()
        self.assertEqual(expected, mappings)
