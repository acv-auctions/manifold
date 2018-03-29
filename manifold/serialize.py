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
THRIFT_BASIC_TYPE_SPEC_LEN = 3
THRIFT_STRUCT_TYPE_SPEC_LEN = 4


def serialize(instance):
    """
    Serializes an object to a dictionary recursively,
    so it can be converted to JSON
    :param instance: any python value or instance
    :return: dictionary serialization of instance
    """
    def to_dict(obj):
        if isinstance(obj, dict):
            return {key: to_dict(value) for key, value in obj.items()}
        elif isinstance(obj, (set, list)):
            return [to_dict(item) for item in obj]

        try:
            return {key: to_dict(value) for key, value in obj.__dict__.items()}
        except AttributeError:
            return obj

    return to_dict(instance)


def _get_spec_for_keyword(t_spec, key):
    for _, arg_spec in t_spec.items():
        if arg_spec[1] == key:
            return arg_spec
    return None


def deserialize(data, ttype):
    """Deserializes a Python dictionary into a `ttype` instance
    :param data:  Python dictionary to parse
    :param ttype: Thriftpy generated class to parse into
    :return: instance of ttype
    """
    spec = ttype.thrift_spec

    struct = ttype()

    for key, value in data.items():
        arg_spec = _get_spec_for_keyword(spec, key)
        if not arg_spec:
            raise KeyError(f"Got unexpected key '{key}'")

        if len(arg_spec) == THRIFT_BASIC_TYPE_SPEC_LEN:
            setattr(struct, key, value)

        if len(arg_spec) == THRIFT_STRUCT_TYPE_SPEC_LEN:
            sub_ttype = arg_spec[2]
            sub_value = deserialize(value, sub_ttype)
            setattr(struct, key, sub_value)

    return struct
