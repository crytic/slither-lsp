import io
import sys
from typing import List, Optional, TextIO

from slither_lsp.servers.base_server import BaseServer
from slither_lsp.state.capabilities import Capabilities


class NullStringIO(io.StringIO):
    """
    I/O implementation which captures output, and optionally mirrors it to the original I/O stream it replaces.
    """

    def write(self, s):
        """
        The write operation for this StringIO does nothing.
        :param s: The provided string which should be written to IO (but is discarded).
        :return: None
        """
        pass

    def writelines(self, __lines: List[str]) -> None:
        """
        The writelines operation for this IO is overridden to do nothing.
        :param __lines: A list of lines to be discarded.
        :return: None
        """
        pass


class ConsoleServer(BaseServer):
    """
    Provides a console (stdin/stdout) interface for JSON-RPC
    """
    def __init__(self, server_capabilities: Capabilities = None):
        self._actual_stdin: Optional[TextIO] = None
        self._actual_stdout: Optional[TextIO] = None
        self._actual_stderr: Optional[TextIO] = None
        super().__init__(server_capabilities=server_capabilities)

    def start(self):
        """
        Starts the server to begin accepting and processing command_handlers on the given IO.
        :return: None
        """
        # Fetch our stdio handles which we will use to communicate, then
        self._actual_stdin = sys.stdin
        self._actual_stdout = sys.stdout
        self._actual_stderr = sys.stderr

        # Now that we have backed up the stdio handles, globally redirect stdout/stderr to a null
        # stream so that all other code which could print does not disturb server communications.
        sys.stdin = NullStringIO()
        sys.stdout = NullStringIO()
        sys.stderr = NullStringIO()

        # Start our server using stdio in binary mode for the provided IO handles.
        self._main_loop(self._actual_stdin.buffer, self._actual_stdout.buffer)

    def stop(self):
        """
        Stops the server from processing commands and restores the previously suppressed stdio handles.
        :return: None
        """
        # If execution has ceased, restore the stdio file handles so that printing can resume as usual.
        sys.stdin = self._actual_stdin
        sys.stdout = self._actual_stdout
        sys.stderr = self._actual_stderr
