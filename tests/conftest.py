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
import django
from django.conf import settings

from tests import settings as test_settings


def pytest_configure(config):  # pylint: disable=W0613
    # Set DJANGO_SETTINGS_MODULE for tests

    settings.configure(default_settings=test_settings)

    django.setup()
