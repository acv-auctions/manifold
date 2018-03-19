import django
from django.conf import settings

from tests import settings as test_settings


def pytest_configure(config):  # pylint: disable=W0613
    # Set DJANGO_SETTINGS_MODULE for tests

    settings.configure(default_settings=test_settings)

    django.setup()
