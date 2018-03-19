from django.test import TestCase

from manifold.file import load_module
from manifold.serialize import serialize


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
