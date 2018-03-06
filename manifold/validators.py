from inspect import isclass

from django import forms
from django.core.exceptions import ValidationError

from manifold.serialize import serialize


class ThriftValidator(forms.Form):
    """
    Base Validator for Thrift Structs.
    Expand upon this like you would a Django Form.
    """
    def __init__(self, struct, *args, **kwargs):
        """Serializes Thrift struct if needed so it can be cleaned
        """
        self.struct = struct
        if not isinstance(struct, dict):
            struct = serialize(struct)
        super().__init__(struct, *args, **kwargs)

    def get(self, key, default=None):
        return self.cleaned_data.get(key, default)


class I16Field(forms.IntegerField):

    MIN_VALUE = -32768
    MAX_VALUE = 32767

    def __init__(self, *args, **kwargs):
        kwargs['max_value'] = self.MAX_VALUE
        kwargs['min_value'] = self.MIN_VALUE
        super().__init__(*args, **kwargs)


class I32Field(forms.IntegerField):

    MIN_VALUE = -2147483648
    MAX_VALUE = 2147483647

    def __init__(self, *args, **kwargs):
        kwargs['max_value'] = self.MAX_VALUE
        kwargs['min_value'] = self.MIN_VALUE
        super().__init__(*args, **kwargs)


class I64Field(forms.IntegerField):
    """No check needed, as pretty much any value will be less than max
    """
    pass


class BoolField(forms.BooleanField):
    """
    Use `required=True` to force always true, or
    use `required=False` to force either T/F
    """
    pass


class DoubleField(forms.IntegerField):
    pass


class StringField(forms.CharField):
    pass


class ByteField(forms.IntegerField):

    def __init__(self, **kwargs):
        kwargs['max_value'] = 255
        kwargs['min_value'] = 0
        super().__init__(**kwargs)


class ListField(forms.Field):
    """Thrift Validator Field to validate a list object
    """

    def __init__(self, *args, list_type=None,
                 min_length=0, max_length=None, **kwargs):
        self.list_type = list_type
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)

        if not self.required and value is None:
            return value

        if not isinstance(value, list):
            raise ValidationError('ListField expected a list.')

        if len(value) < self.min_length:
            raise ValidationError(
                f'ListField expected at least {self.min_length} items.'
            )

        if self.max_length and len(value) > self.max_length:
            raise ValidationError(
                f'ListField expected at most {self.max_length} items.'
            )

        if self.list_type:
            for index in value:
                if not isinstance(index, self.list_type):
                    raise ValidationError(
                        f'ListField expected "{self.list_type}" items.'
                    )

        return value


class SetField(forms.Field):
    """Thrift Validator Field to validate a set container
    """

    def __init__(self, *args,
                 set_type=None, min_length=0, max_length=None, **kwargs):
        self.set_type = set_type
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)

        if not self.required and value is None:
            return value

        if not isinstance(value, (list, set)):
            raise ValidationError('SetField expected a list.')

        if len(value) < self.min_length:
            raise ValidationError(
                f'SetField expected at least {self.min_length} items.'
            )

        if self.max_length and len(value) > self.max_length:
            raise ValidationError(
                f'ListField expected at most {self.max_length} items.'
            )

        if self.set_type:
            for index in value:
                if not isinstance(index, self.set_type):
                    raise ValidationError(
                        f'SetField expected "{self.set_type}" items.'
                    )

        return set(value)


class MapField(forms.Field):
    """Django Form Field to validate a dict object

    Use `key_type` and `val_type` to enforce type mappings
    """

    def __init__(self, *args, key_type=None, val_type=None, **kwargs):
        self.key_type = key_type
        self.val_type = val_type
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if not self.required and value is None:
            return value

        if not isinstance(value, dict):
            raise ValidationError('MapField expected a dictionary.')

        if self.key_type or self.val_type:
            for key, val in value.items():
                if self.key_type and not isinstance(key, self.key_type):
                    raise ValidationError(
                        f'All MapField keys must be {self.key_type}'
                    )
                if self.val_type and not isinstance(val, self.val_type):
                    raise ValidationError(
                        f'All MapField vals must be {self.val_type}'
                    )
        return value


class StructField(forms.Field):

    def __init__(self, validator_class, *args, **kwargs):
        if not isclass(validator_class) or \
                not issubclass(validator_class, ThriftValidator):
            raise TypeError(
                'StructField first argument must be ThriftValidator subclass!'
            )
        self.validator_class = validator_class
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        validator = self.validator_class(value)
        if not validator.is_valid():
            errors = {field: err for field, err in validator.errors.items()}
            raise ValidationError(
                f'{self.validator_class} failed validation: {errors}'
            )

        return validator.cleaned_data
