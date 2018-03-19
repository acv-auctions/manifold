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


def new(ttype, *args, key='default', **kwargs):
    """Shortcut to create thrift structs
    :param key: Thrift settings key to load
    :param ttype: Thrift struct name as a string
    :param args: Args to pass to constructor
    :param kwargs: kwargs to pass to constructor
    :return: instantiated object of `ttype`
    """
    return getattr(load_module(key), ttype)(*args, **kwargs)
