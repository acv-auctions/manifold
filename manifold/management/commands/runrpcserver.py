from django.core.management.base import BaseCommand

from manifold import rpc


class Command(BaseCommand):
    """Run a development thrift server"""

    def handle(self, *args, **options):

        rpc.make_server()
