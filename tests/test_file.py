from django.test import TestCase

from manifold.file import thrift_module, new
from manifold.serialize import serialize


class FileTestSuite(TestCase):

    def test_thrift_module(self):
        struct = thrift_module.ExampleStruct(
            test_string="hello",
            test_bool=True
        )
        self.assertEqual(struct.test_string, "hello")
        self.assertTrue(struct.test_bool)

    def test_default_thrift_module(self):
        struct = thrift_module.ExampleStruct(test_string="hello")
        self.assertEqual(struct.test_string, "hello")
        self.assertTrue(struct.test_bool)

    def test_new(self):
        expected = thrift_module.ExampleStruct(test_string="hello")
        result = new('ExampleStruct', test_string="hello")
        self.assertEqual(expected, result)


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

        expected = {
            'some_string': 'hello world',
            'innerStruct': {
                'val': 123,

            }
        }
        test_struct = new(
            'ContainedStruct',
            some_string='hello world',
            innerStruct=new('InnerStruct', val=123,)
        )

        result = serialize(test_struct)
        self.assertEqual(result, expected)
