import os

from django.core.management.base import BaseCommand

from manifold import rpc


class Command(BaseCommand):
    """Run a development thrift server"""

    def handle(self, *args, **options):
        if os.environ.get('RUN_MAIN') == 'true':
            return
        rpc.make_server()
