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
import codecs
import os
import re
import sys
from setuptools import find_packages, setup

DESCRIPTION = "A python library that implements a thrift parser into Django to use it's models and controllers to " \
              "implement RPC/HTTP services. "

EXCLUDE_PACKAGES = [
    "*.tests",
    "*.tests.*",
    "tests.*",
    "tests",
]


def read(*parts):
    with codecs.open(os.path.join(cwd, *parts), 'r') as fp:
        return fp.read()


def find_info(*file_paths, info='version'):
    """ Get __{info}__ from a list of file paths
    """
    version_file = read(*file_paths)
    version_match = re.search(f"^__{info}__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def confirm(prompt, expected=('yes', 'y')):
    """ Prompts the user to continue with the script
    :param prompt: What to show the user
    :param expected: Valid answers to continue
    :return:
    """
    response = input(prompt + f": ({'/'.join(expected)}) ")
    if response.lower() not in expected:
        print("  Quitting due to invalid prompt answer.")
        return exit(1)


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

cwd = os.path.abspath(os.path.dirname(__file__))

version = find_info("manifold", "__init__.py", info='version')

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


confirm('Did you run `make testlint`?')
confirm(f'Did you increment the version? Currently {version}')
confirm(f'Did you create a new branch called v{version}?')
confirm(f'Did you create a new release called v{version} from that branch?')

setup(
    name=find_info("manifold", "__init__.py", info='title'),
    version=version,
    packages=find_packages(exclude=EXCLUDE_PACKAGES),
    include_package_data=True,
    license='Apache 2.0 License',
    description=DESCRIPTION,
    long_description=README,
    url='https://www.acvauctions.com',
    author=find_info("manifold", "__init__.py", info='author'),
    author_email=find_info("manifold", "__init__.py", info='email'),
    install_requires=[
        'Django==2.0.2',
        'gunicorn-thrift==0.2.21',
        'thriftpy==0.3.9'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
