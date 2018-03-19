#! /usr/bin/env python
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
import os
import subprocess
import sys

import pytest


PYTEST_ARGS = {
    'default': ['tests', '--tb=short', '-s', '-rw'],
    'fast': ['tests', '--tb=short', '-q', '-s', '-rw'],
}

PYLINT_ARGS = ['manifold', 'tests']


def exit_on_failure(ret, message=None):
    if ret:
        os._exit(ret)


def pylint_main(args):
    print('Running pylint code linting')
    ret = subprocess.call(['pylint'] + args)
    print('pylint failed' if ret else 'pylint passed')
    return ret


def split_class_and_function(string):
    class_string, function_string = string.split('.', 1)
    return "%s and %s" % (class_string, function_string)


def is_function(string):
    # `True` if it looks like a test function is included in the string.
    return string.startswith('test_') or '.test_' in string


def is_class(string):
    # `True` if first character is uppercase - assume it's a class name.
    return string[0] == string[0].upper()


if __name__ == "__main__":
    try:
        sys.argv.remove('--nolint')
    except ValueError:
        run_pylint = True
        run_isort = True
    else:
        run_pylint = False
        run_isort = False

    try:
        sys.argv.remove('--lintonly')
    except ValueError:
        run_tests = True
    else:
        run_tests = False

    try:
        sys.argv.remove('--fast')
    except ValueError:
        style = 'default'
    else:
        style = 'fast'
        run_pylint = False
        run_isort = False

    if len(sys.argv) > 1:
        pytest_args = sys.argv[1:]
        first_arg = pytest_args[0]

        try:
            pytest_args.remove('--coverage')
        except ValueError:
            pass
        else:
            pytest_args = [
                '--cov-report',
                'xml',
                '--cov',
                'manifold'] + pytest_args

        if first_arg.startswith('-'):
            # `runtests.py [flags]`
            pytest_args = ['tests'] + pytest_args
        elif is_class(first_arg) and is_function(first_arg):
            # `runtests.py TestCase.test_function [flags]`
            expression = split_class_and_function(first_arg)
            pytest_args = ['tests', '-k', expression] + pytest_args[1:]
        elif is_class(first_arg) or is_function(first_arg):
            # `runtests.py TestCase [flags]`
            # `runtests.py test_function [flags]`
            pytest_args = ['tests', '-k', pytest_args[0]] + pytest_args[1:]
    else:
        pytest_args = PYTEST_ARGS[style]

    if run_tests:
        exit_on_failure(pytest.main(pytest_args))

    if run_pylint:
        exit_on_failure(pylint_main(PYLINT_ARGS))

    os._exit(0)
