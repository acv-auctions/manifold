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
from django.test import TestCase

from manifold.file import load_module, load_service
from manifold.serialize import serialize, deserialize


class FileTestSuite(TestCase):

    thrift_module = load_module()

    def test_thrift_module(self):
        struct = self.thrift_module.ExampleStruct(
            test_string="hello",
            test_bool=True
        )
        self.assertEqual(struct.test_string, "hello")
        self.assertTrue(struct.test_bool)

    def test_default_thrift_module(self):
        struct = self.thrift_module.ExampleStruct(test_string="hello")
        self.assertEqual(struct.test_string, "hello")
        self.assertTrue(struct.test_bool)

    def test_not_default(self):
        thrift = load_module('non-default')
        struct = thrift.Secondary(val=64)
        self.assertEqual(struct.val, 64)

    def test_load_service_default(self):
        expected_func_args = [
            'multiVarArgument_args',
            'pingPong_args',
            'pong_args',
            'simple_args',
            'complex_args'
        ]
        service = load_service()
        self.assertTrue(
            all([hasattr(service, x) for x in expected_func_args])
        )

    def test_load_service_key(self):
        expected_func_args = [
            'deadFunction_args'
        ]
        service = load_service(key='non-default')
        self.assertTrue(
            all([hasattr(service, x) for x in expected_func_args])
        )


class SerializeTestSuite(TestCase):

    def test_primitive_serializer(self):

        expected = [1, 2, 3]
        result = serialize([1, 2, 3])
        self.assertEqual(expected, result)

        expected = 5
        result = serialize(5)
        self.assertEqual(expected, result)

        expected = None
        result = serialize(None)
        self.assertEqual(expected, result)

        expected = {'hello': 'world', 'nested': {'woah': 'baby'}}
        result = serialize(expected)
        self.assertEqual(expected, result)

    def test_object_serializer(self):
        module = load_module()

        expected = {
            'some_string': 'hello world',
            'innerStruct': {
                'val': 123,

            }
        }
        test_struct = module.ContainedStruct(
            some_string='hello world',
            innerStruct=module.InnerStruct(val=123,)
        )

        result = serialize(test_struct)
        self.assertEqual(result, expected)


class DeserializeTestSuite(TestCase):

    def test_deserialize_type(self):
        ttype = load_module().ExampleStruct
        data = {
            'test_string': 'Hello World',
            'test_bool': False
        }

        expected = load_module().ExampleStruct(
            test_string='Hello World',
            test_bool=False
        )

        self.assertEqual(expected, deserialize(data, ttype))

    def test_inner_struct_type(self):
        module = load_module()
        ttype = module.ContainedStruct
        data = {
            'some_string': 'Hello World',
            'innerStruct': {
                'val': 123
            }
        }

        expected = ttype(
            some_string='Hello World',
            innerStruct=module.InnerStruct(val=123)
        )

        self.assertEqual(expected, deserialize(data, ttype))

    def test_invalid_key_given(self):
        module = load_module()
        ttype = module.ContainedStruct
        data = {
            'some_string': 'Hello World',
            'innerStruct': {
                'val': 123
            },
            'invalid_key': 'What am I doing here?'
        }

        with self.assertRaises(KeyError):
            deserialize(data, ttype)
