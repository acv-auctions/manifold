import django


def pytest_configure(config):  # pylint: disable=W0613
    # Set DJANGO_SETTINGS_MODULE for tests
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SECRET_KEY='not very secret in tests',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'manifold',
        ),
        THRIFT={
            'FILE': 'tests/example.thrift',
            'SERVICE': 'ExampleService'
        }
    )

    django.setup()
