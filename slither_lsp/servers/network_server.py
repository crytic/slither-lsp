import socket
from threading import Thread
from typing import Optional

from slither_lsp.servers.base_server import BaseServer
from slither_lsp.types.lsp_capabilities import ServerCapabilities


class NetworkServer(BaseServer):
    """
    Provides a TCP network socket interface for JSON-RPC
    """
    def __init__(self, port: int, server_capabilities: ServerCapabilities = None):
        # Set our port and initialize our socket
        self.port = port
        self._server_socket: Optional[socket] = None
        self._thread: Optional[Thread] = None
        super().__init__(server_capabilities=server_capabilities)

    def start(self):
        """
        Starts the server to begin accepting and processing command_handlers on the given IO.
        :return: None
        """
        # Create a socket to accept our connections
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind our socket
        # TODO: For now we only allow one connection, determine if we should allow multiple in the future.
        self._server_socket.bind(('127.0.0.1', self.port))
        self._server_socket.listen(1)

        # Accept connections on another thread.
        self._thread = Thread(
            target=self._accept_connections,
            args=()
        )
        self._thread.start()

    def _accept_connections(self):
        """
        A blocking function which accepts incoming connections and begins processing commands.
        :return: None
        """
        # Accept connections and process with the underlying IO handlers.
        while True:
            # Accept a new connection, create a file handle which we will use to process our main loop
            connection_socket, address = self._server_socket.accept()
            connection_file_handle = connection_socket.makefile(mode='rwb', encoding='utf-8')

            # Enter the main loop, this will reset state, so each connection will reset state.
            self._main_loop(connection_file_handle, connection_file_handle)

    def stop(self):
        """
        Stops the server from processing commands and tears down the underlying socket.
        :return: None
        """
        # TODO: Kill thread, etc.
        self._server_socket.close()
