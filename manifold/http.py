import importlib
import json
import logging

import thriftpy
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from manifold.file import load_service
from manifold.handler import handler
from manifold.serialize import serialize, deserialize

logger = logging.getLogger(__name__)


def _parse_json_args_to_list(thrift_spec, json_data):
    """
    Parses a Python dictionary into an array of Thrift structs and
    types requested, in the correct order.

    thrift_spec is a dictionary where the key is the arg ordering,
    starting at 1, and the value is a tuple of:
    (size, arg_name, <Expected Struct>, False)

    The second index (Expected Struct) is not always present, only
    if its a complex argument like a struct. The final index is a
    boolean used internally by Thriftpy for checking.

    :param thrift_spec: Thriftpy Thrift class thrift_spec
    :param json_data: Dictionary to parse through
    :return: list of Thrift types/structs matching thrift_spec
    """
    arg_list = []

    current_index = 1  # Thrift args start counting at one
    while current_index in thrift_spec:

        # Pull the spec and the argument name for
        # that specific argument
        spec = thrift_spec[current_index]
        expected_key_name = spec[1]

        # Caught and thrown to provide clearer error message
        if expected_key_name not in json_data:
            raise KeyError(f'Expected {expected_key_name} argument.')
        data = json_data[expected_key_name]

        # If current spec contains a struct type or not
        if len(spec) == 3:  # Basic type
            arg_list.append(data)
        else:  # Complex struct type
            ttype = spec[2]
            arg = deserialize(data, ttype)
            arg_list.append(arg)
        current_index += 1
    return arg_list


def _handle_arg_function(handler_func, request, thrift_args):
    """Parse, deserialize, and call RPC handler from Django request
    :param handler_func: Thrift handler function (the decorated function)
    :param request: Django request with body
    :param thrift_args: Thrift function arguments from the service.thrift_spec
    :return: Dictionary serialized response from RPC function
    """
    try:  # Try to load any params given
        data = json.loads(request.body)
    except ValueError:
        data = None

    arguments = _parse_json_args_to_list(thrift_args, data)

    return serialize(handler_func(*arguments))


def wrap_thrift_function(name, handler_function):
    """Wraps a Thrift handler function in a Django
    :param name: The RPC function name that was called
    :param handler_function: Thrift function to handle RPC
    :return: Function that can be called with path()
    """
    service = load_service()
    thrift_args = getattr(service, f'{name}_args').thrift_spec

    @csrf_exempt
    def request_handler(request):
        """The request handler Django uses for each call
        :param request: Django request
        :return: Django JsonResponse
        """
        try:  # Run the thrift handler function with JSON kwargs
            if thrift_args:
                response = _handle_arg_function(
                    handler_function,
                    request,
                    thrift_args
                )
            else:
                response = serialize(handler_function())

        except KeyError as exc:
            logger.error(
                f"Invalid HTTP args to '{name}': {str(exc)}"
            )
            return JsonResponse({
                'response': 'error',
                'error': str(exc)
            })

        except TypeError as exc:
            logger.error(
                f"Invalid HTTP args to '{name}': {str(exc)}"
            )
            error = 'Invalid Thrift request.'
            if 'unexpected' in str(exc):
                error = 'Unable to coerce keywords into handler.'
            elif 'required' in str(exc):
                error = 'Missing Thrift keys.'
            return JsonResponse({'response': 'error', 'error': error})

        except thriftpy.thrift.TException as exc:  # Handle Thrift Exceptions
            return JsonResponse({
                'response': 'error',
                'exception': serialize(exc),
                'exceptionType': str(type(exc).__name__)
            })

        return JsonResponse({'return': response, 'response': 'ok'}, safe=False)

    return request_handler


def build_urls():
    """Builds `urlpatterns` for Django to serve using the Manifold
    ServiceHandler. This loads any apps it can and adds their routes
    :return: List of Django paths()
    """
    for i_app in settings.INSTALLED_APPS:
        if i_app.startswith('django') or 'manifold' in i_app:
            continue
        try:
            importlib.import_module("%s.views" % i_app)
        except ImportError:
            logger.info(
                'No module "%s.views" found, skipping RPC calls from it...',
                i_app
            )

    patterns = []
    mappings = handler.get_current_mappings()
    for name, handler_function in mappings.items():
        patterns.append(
            path(
                name,
                wrap_thrift_function(name, handler_function),
                name="name"
            )
        )
    return patterns


urlpatterns = build_urls()

# Create the WSGI application
application = get_wsgi_application()
