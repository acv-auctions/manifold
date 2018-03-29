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
import importlib
import logging

import django
from django.conf import settings
try:
    from newrelic import agent
except ImportError:
    agent = None
from thriftpy.protocol import TBinaryProtocolFactory
from thriftpy.rpc import make_client as thrift_client
from thriftpy.server import TThreadedServer
from thriftpy.thrift import TProcessor
from thriftpy.transport import (
    TBufferedTransportFactory,
    TServerSocket,
    TSSLServerSocket,
)

from manifold.handler import handler
from manifold.file import load_service


# Ensure settings are read
django.setup()


__new_relic = False


def _print_rpc_config():
    if handler.configured:
        return
    print('\n** Manifold RPC --> Function Mappings **')
    handler.print_current_mappings()
    print()
    handler.configured = True


def get_rpc_application():
    """Creates a Gunicorn Thrift compatible TProcessor and initializes NewRelic
    """
    global __new_relic

    if agent and not __new_relic:
        try:
            agent.initialize()
            logging.info('Initialized New Relic application')
            __new_relic = True
        except Exception as exc:  # pylint: disable=all
            logging.warning(
                'Could not wrap RPC server in New Relic config. Exc: %s',
                exc
            )

    for i_app in settings.INSTALLED_APPS:
        if i_app.startswith('django') or 'manifold' in i_app:
            continue
        try:
            importlib.import_module("%s.views" % i_app)
        except ImportError:
            logging.info(
                'No module "%s.views" found, skipping RPC calls from it...',
                i_app
            )

    _print_rpc_config()

    return TProcessor(load_service(), handler)


def make_server(host="localhost", port=9090, unix_socket=None,
                proto_factory=TBinaryProtocolFactory(),
                trans_factory=TBufferedTransportFactory(),
                client_timeout=3000, certfile=None):
    """Creates a Thrift RPC server and serves it with configuration
    """
    processor = get_rpc_application()

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

    try:
        return server
    except KeyboardInterrupt:
        print()
        print("Stopping Server from Keyboard Interruption")
        exit()


def make_client(key='default'):
    """Creates a client to call functions with
    :param key: Settings key to create client with
    :return: Thriftpy client
    """
    thrift_settings = settings.MANIFOLD[key]
    host = thrift_settings.get('host', '127.0.0.1')
    port = thrift_settings.get('port', 9090)
    return thrift_client(load_service(key), host=host, port=port)
