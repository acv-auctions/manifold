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
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import autoreload

from manifold import rpc


def get_manifold_version():
    import manifold
    return manifold.__version__


class Command(BaseCommand):
    """Run a development thrift server"""

    def add_arguments(self, parser):
        parser.add_argument('host', type=str, nargs='?', default='127.0.0.1')
        parser.add_argument('port', type=int, nargs='?', default=9090)

    def run_server(self, host, port):
        autoreload.raise_last_exception()
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

        self.stdout.write(
            f"Django Manifold version {get_manifold_version()}\n"
            f"Django version {self.get_version()}, "
            f"using settings {settings.SETTINGS_MODULE}\n"
            f"Starting development RPC server at {host}:{port}\n"
            f"Quit the server with {quit_command}.\n"
        )

        server = rpc.make_server()
        server.serve()

    def handle(self, *args, **options):
        host = options.get('host', '127.0.0.1')
        port = options.get('port', 9090)

        # self.run_server(host, port)

        autoreload.main(self.run_server, args=(host, port), kwargs=None)
