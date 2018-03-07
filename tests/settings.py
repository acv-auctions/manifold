DEBUG_PROPAGATE_EXCEPTIONS = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
SECRET_KEY = 'not very secret in tests'
INSTALLED_APPS = [
    'manifold'
]
THRIFT = {
    'FILE': 'tests/example.thrift',
    'SERVICE': 'ExampleService'
}
