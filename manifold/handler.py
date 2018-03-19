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
            print(f'* {mapped_name} -- {getattr(self, mapped_name).__name__}')

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
