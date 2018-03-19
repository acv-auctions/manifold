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
from django.apps import apps
from django.test import TestCase

from manifold.apps import ManifoldConfig


class AppTestSuite(TestCase):

    def test_apps(self):
        self.assertEqual(ManifoldConfig.name, 'manifold')
        self.assertEqual(apps.get_app_config('manifold').name, 'manifold')
