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
import logging

try:
    from newrelic import agent
except ImportError:
    agent = None


class ServiceHandler:
    """
    The Service Handler maps functions to Thrift functions, and is responsible
    for serving them once the server starts.
    """

    instance = None
    configured = False

    def __init__(self):
        self.__mapped_names = set()

    def map_function(self, name):
        """Map a Python function to a Thrift function
        """
        def decorator(func):

            # Check if the Thrift function was already assigned
            if name in self.__mapped_names:
                raise NameError(
                    f'Thrift Function "{name}" is already assigned!'
                )

            self.__mapped_names.add(name)

            setattr(self, name, func)
            return func

        return decorator

    def print_current_mappings(self):
        for mapped_name in self.__mapped_names:
            func = getattr(self, mapped_name)
            name = f'{func.__module__}.{func.__name__}'
            print(f'* {mapped_name} -- {name}')

    def get_current_mappings(self):
        return {name: getattr(self, name) for name in self.__mapped_names}

    def __getattribute__(self, name):
        """Overridden to set the New Relic transaction name if handler.
        """
        if agent and '__mapped_names' not in name and name in self.__mapped_names:
            try:
                agent.set_transaction_name(name)
            except: # pylint: disable=all
                logging.warning(
                    'Could not set New Relic transaction name. '
                    'Is it installed and configured?'
                )

        return object.__getattribute__(self, name)


def __create_handler():
    if not ServiceHandler.instance:
        ServiceHandler.instance = ServiceHandler()
    return ServiceHandler.instance


handler = __create_handler()
