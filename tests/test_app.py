from django.apps import apps
from django.test import TestCase

from manifold.apps import ManifoldConfig


class AppTestSuite(TestCase):

    def test_apps(self):
        self.assertEqual(ManifoldConfig.name, 'manifold')
        self.assertEqual(apps.get_app_config('manifold').name, 'manifold')
