from django.test import TestCase

from manifold import validators
from manifold.file import new
from manifold.serialize import serialize


class I16FieldTestSuite(TestCase):

    class I16Validator(validators.ThriftValidator):
        test_i16 = validators.I16Field()

    def test_I16Field(self):
        valid = self.I16Validator({'test_i16': 123})
        self.assertTrue(valid.is_valid())

    def test_I16Invalid(self):
        valid = self.I16Validator({'test_i16': 999999})
        self.assertFalse(valid.is_valid())


class I32FieldTestSuite(TestCase):

    class I32Validator(validators.ThriftValidator):
        test_i32 = validators.I32Field()

    def test_I32Field(self):
        valid = self.I32Validator({'test_i32': 999999})
        self.assertTrue(valid.is_valid())

    def test_I32Invalid(self):
        valid = self.I32Validator({'test_i32': 21474836478})
        self.assertFalse(valid.is_valid())


class SetFieldTestSuite(TestCase):

    class SetValidator(validators.ThriftValidator):
        test_set = validators.SetField(set_type=int)

    def test_SetField(self):
        valid = self.SetValidator({'test_set': {1, 2, 3}})
        self.assertTrue(valid.is_valid())

    def test_SetInvalid(self):
        valid = self.SetValidator({'test_set': {1, 'hello', 1}})
        self.assertFalse(valid.is_valid())


class BoolFieldTestSuite(TestCase):

    class BoolTrueValidator(validators.ThriftValidator):
        bool = validators.BoolField(required=True)

    class BoolValidator(validators.ThriftValidator):
        bool = validators.BoolField(required=False)

    def test_always_BoolField(self):
        valid = self.BoolTrueValidator({'bool': True})
        self.assertTrue(valid.is_valid())

        valid = self.BoolTrueValidator({'bool': False})
        self.assertFalse(valid.is_valid())

    def test_BoolField(self):
        valid = self.BoolValidator({'bool': True})
        self.assertTrue(valid.is_valid())

        valid = self.BoolValidator({'bool': False})
        self.assertTrue(valid.is_valid())


class ByteFieldTestSuite(TestCase):

    class ByteValidator(validators.ThriftValidator):
        byte = validators.ByteField()

    def test_ByteField(self):
        valid = self.ByteValidator({'byte': 128})
        self.assertTrue(valid.is_valid())

    def test_invalid_ByteField(self):
        invalid = self.ByteValidator({'byte': 300})
        self.assertFalse(invalid.is_valid())

        invalid = self.ByteValidator({'byte': -50})
        self.assertFalse(invalid.is_valid())


class ListFieldTestSuite(TestCase):

    class ListValidator(validators.ThriftValidator):
        field = validators.ListField(list_type=int, min_length=2)

    class ListNotRequiredValidator(validators.ThriftValidator):
        field = validators.ListField(list_type=int, required=False)
        test = validators.I16Field(required=False)

    def test_ListField_valid(self):
        valid_form = self.ListValidator({'field': [1, 2, 3]})
        self.assertTrue(valid_form.is_valid())

    def test_ListField_bad_item(self):
        bad_item_type = self.ListValidator({'field': [1, 'hello']})
        self.assertFalse(bad_item_type.is_valid())

    def test_ListField_bad_type(self):
        bad_type = self.ListValidator({'field': {}})
        self.assertFalse(bad_type.is_valid())

    def test_ListField_bad_length(self):
        bad_length = self.ListValidator({'field': [0]})
        self.assertFalse(bad_length.is_valid())

    def test_ListValidator_not_required_fields_valid(self):
        valid_form = self.ListNotRequiredValidator(
            {'field': [1, 2, 3], 'test': 0}
        )
        self.assertTrue(valid_form.is_valid())

    def test_ListValidator_not_required_fields_None(self):
        valid_empty_form = self.ListNotRequiredValidator({'test': 0})
        self.assertTrue(valid_empty_form.is_valid())


class MapFieldTestSuite(TestCase):

    class MapValidator(validators.ThriftValidator):
        field = validators.MapField()

    class MapNotRequiredValidator(validators.ThriftValidator):
        field = validators.MapField(required=False)
        test = validators.I16Field(required=False)

    def test_MapField_invalid_empty(self):
        valid_empty_form = self.MapValidator({'field': {}})
        self.assertFalse(valid_empty_form.is_valid())

    def test_MapField_valid(self):
        valid_form = self.MapValidator({'field': {'hello': 'world'}})
        self.assertTrue(valid_form.is_valid())

    def test_MapField_invalid(self):
        bad_type = self.MapValidator({'field': []})
        self.assertFalse(bad_type.is_valid())

    def test_MapValidator_not_required_fields_valid(self):
        valid_form = self.MapNotRequiredValidator({'field': {}, 'test': 0})
        self.assertTrue(valid_form.is_valid())

    def test_MapValidator_not_required_fields_None(self):
        valid_empty_form = self.MapNotRequiredValidator({'test': 0})
        self.assertTrue(valid_empty_form.is_valid())


class InnerStructValidator(validators.ThriftValidator):
    val = validators.I16Field()


class ThriftValidatorTestSuite(TestCase):

    class SomeValidator(validators.ThriftValidator):
        test_string = validators.StringField()

    class ComplexValidator(validators.ThriftValidator):
        some_string = validators.StringField()
        innerStruct = validators.StructField(InnerStructValidator)

    def test_validator_init_struct(self):
        thrift_struct = new('ExampleStruct', test_string='hello')
        form = self.SomeValidator(thrift_struct)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get('test_string'), 'hello')

    def test_validator_init_dict(self):
        thrift_struct = new('ExampleStruct', test_string='hello')
        form = self.SomeValidator(serialize(thrift_struct))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get('test_string'), 'hello')

    def test_validator_get(self):
        valid_form = self.SomeValidator({'test_string': 'hello'})
        valid_form.is_valid()
        self.assertEqual(valid_form.get('test_string'), 'hello')
        self.assertFalse(valid_form.get('test_miss', default=False))

    def test_inner_struct_validator(self):
        i_struct = new('InnerStruct', val=123)
        thrift_struct = new(
            'ContainedStruct',
            some_string='hello',
            innerStruct=i_struct
        )

        validator = self.ComplexValidator(thrift_struct)
        self.assertTrue(validator.is_valid(), validator.errors)

        self.assertEqual(validator.get('innerStruct').get('val'), 123)

    def test_inner_struct_validator_invalid(self):
        i_struct = new('InnerStruct', val=999999)
        thrift_struct = new(
            'ContainedStruct',
            some_string='hello',
            innerStruct=i_struct
        )

        validator = self.ComplexValidator(thrift_struct)
        self.assertFalse(validator.is_valid(), validator.errors)
