import os

from django.conf import settings
import thriftpy

if not os.getenv("DJANGO_SETTINGS_MODULE", None):  # pragma: no cover
    raise ValueError("'DJANGO_SETTINGS_MODULE' environment variable must exist!")

thrift_module = thriftpy.load(
    settings.THRIFT["FILE"],
    module_name=settings.THRIFT["FILE"].replace('.', '_')
)

thrift_service = getattr(thrift_module, settings.THRIFT["SERVICE"])
