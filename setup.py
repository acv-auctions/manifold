import os
from setuptools import find_packages, setup

DESCRIPTION = "A python library that implements a thrift parser into Django to use it's models and controllers to " \
              "implement RPC/HTTP services. "

EXCLUDE_PACKAGES = [
    "*.tests",
    "*.tests.*",
    "tests.*",
    "tests",
]

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-manifold',
    version='1.1',
    packages=find_packages(exclude=EXCLUDE_PACKAGES),
    include_package_data=True,
    license='BSD License',  # example license
    description=DESCRIPTION,
    long_description=README,
    url='https://www.acvauctions.com',
    author='Daniel Starner',
    author_email='dstarner@acvauctions.com',
    install_requires=[
        'Django==2.0.2',
        'gunicorn-thrift==0.2.21',
        'thriftpy==0.3.9'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
