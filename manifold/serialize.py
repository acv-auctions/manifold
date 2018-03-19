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
