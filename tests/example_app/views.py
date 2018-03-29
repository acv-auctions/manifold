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
from manifold.file import load_module
from manifold.handler import handler

from .validators import ComplexValidator, InnerStructValidator


@handler.map_function('pingPong')
def handle_ping_pong(val):

    if val == 5:
        return True

    return False


@handler.map_function('pong')
def handle_pong():
    return


@handler.map_function('simple')
def handle_simple(val):
    module = load_module()

    validator = InnerStructValidator(val)
    if not validator.is_valid():
        raise module.ExampleException(error='Woah')

    return module.ContainedStruct(
        innerStruct=module.InnerStruct(val=234),
        some_string='Hello World'
    )


@handler.map_function('complex')
def handle_complex(val):
    module = load_module()

    validator = ComplexValidator(val)
    if not validator.is_valid():
        raise module.ExampleException(error=validator.error_str())

    return module.ContainedStruct(
        innerStruct=module.InnerStruct(val=234),
        some_string='Hello World'
    )


@handler.map_function('multiVarArgument')
def handle_multi_var(int1, int2):
    return int1 == int2
