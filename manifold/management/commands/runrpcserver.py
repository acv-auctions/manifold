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

from django.core.management.base import BaseCommand

from manifold import rpc


class Command(BaseCommand):
    """Run a development thrift server"""

    def add_arguments(self, parser):
        parser.add_argument('host', type=str, nargs='?', default='127.0.0.1')
        parser.add_argument('port', type=int, nargs='?', default=9090)

    def handle(self, *args, **options):
        if os.environ.get('RUN_MAIN') == 'true':
            return

        host = options.get('host', '127.0.0.1')
        port = options.get('port', 9090)

        self.stdout.write(
            'Starting Thrift RPC server running @ %s:%s' % (host, port)
        )

        server = rpc.make_server()
        server.serve()
