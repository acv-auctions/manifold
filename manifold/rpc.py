import importlib
import logging

import django
from django.conf import settings
try:
    from newrelic import agent
except ImportError:
    agent = None
from thriftpy.protocol import TBinaryProtocolFactory
from thriftpy.server import TThreadedServer
from thriftpy.thrift import TProcessor
from thriftpy.transport import (
    TBufferedTransportFactory,
    TServerSocket,
    TSSLServerSocket,
)

from manifold.handler import create_handler
from manifold.file import thrift_service


# Ensure settings are read
django.setup()


def create_processor():
    """Creates a Gunicorn Thrift compatible TProcessor and initializes NewRelic
    """

    if agent:
        try:
            agent.initialize()
            logging.info('Initialized New Relic application')
        except Exception as exc:  # pylint: disable=all
            logging.warning(
                'Could not wrap RPC server in New Relic config. Exc: %s',
                exc
            )

    installed_apps = [
        x for x in settings.INSTALLED_APPS if not x.startswith("django")
    ]

    for installed_app in installed_apps:
        try:
            importlib.import_module("%s.views" % installed_app)
        except ImportError:
            logging.info(
                'No module "%s.views" found, skipping RPC calls from it...',
                installed_app
            )

    handler = create_handler()
    print('\n** Manifold RPC Function Mappings **')
    for mapped_name in handler.mapped_names:
        print(f'* {mapped_name} -- {getattr(handler, mapped_name).__name__}')
    print()

    return TProcessor(thrift_service, handler)


def make_server(host="localhost", port=9090, unix_socket=None,
                proto_factory=TBinaryProtocolFactory(),
                trans_factory=TBufferedTransportFactory(),
                client_timeout=3000, certfile=None):
    """Creates a Thrift RPC server and serves it with configuration
    """
    processor = create_processor()

    if unix_socket:
        server_socket = TServerSocket(unix_socket=unix_socket)
        if certfile:
            logging.error("SSL only works with host:port, not unix_socket.")
    elif host and port:
        if certfile:
            server_socket = TSSLServerSocket(
                host=host, port=port, client_timeout=client_timeout,
                certfile=certfile)
        else:
            server_socket = TServerSocket(
                host=host, port=port, client_timeout=client_timeout)
    else:
        raise ValueError("Either host/port or unix_socket must be provided.")

    server = TThreadedServer(processor, server_socket,
                             iprot_factory=proto_factory,
                             itrans_factory=trans_factory)

    print('Starting Thrift RPC server running @ %s:%s' % (host, port))

    try:
        server.serve()
    except KeyboardInterrupt:
        print()
        print("Stopping Server from Keyboard Interruption")
        exit()


app = create_processor()
