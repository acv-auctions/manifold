from django import forms
from django.core.exceptions import ValidationError


class ThriftValidator(forms.Form):
    """
    Base Validator for Thrift Structs.
    Expand upon this like you would a Django Form.
    """
    pass


class ListField(forms.Field):
    """Thrift Validator Field to validate a list object
    """

    def __init__(self, list_type, min_length=0, *args, **kwargs):
        self.list_type = list_type
        self.min_length = min_length
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)

        if not isinstance(value, list):
            raise ValidationError('ListField expected a list.')

        if len(value) < self.min_length:
            raise ValidationError(
                f'ListField expected at least {self.min_length} items.'
            )


class DictField(forms.Field):
    """Django Form Field to validate a dict object
    """

    def clean(self, value):

        if self.required and not isinstance(value, dict):
            raise ValidationError('DictField expected a dictionary.')
