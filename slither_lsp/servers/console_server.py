import sys
from slither_lsp.servers.base_server import BaseServer


class ConsoleServer(BaseServer):
    """
    Provides a console (stdin/stdout) interface for JSON-RPC
    """

    def start(self):
        """
        Starts the server to begin accepting and processing command_handlers on the given IO.
        :return: None
        """
        # Start our server using stdio in binary mode for the provided IO handles.
        self._main_loop(sys.stdin.buffer, sys.stdout.buffer)
