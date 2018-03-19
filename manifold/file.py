from django.conf import settings
import thriftpy


def load_module(key='default'):
    thrift = settings.MANIFOLD[key]
    return thriftpy.load(
        thrift['file'],
        module_name=thrift['file'].replace('.', '_')
    )


def load_service(key='default'):
    module = load_module(key)
    return getattr(module, settings.MANIFOLD[key]['service'])
