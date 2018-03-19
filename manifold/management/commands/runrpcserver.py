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
