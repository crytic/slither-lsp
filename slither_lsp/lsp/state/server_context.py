from typing import Optional

from pkg_resources import require
from slither_lsp.lsp.types.basic_structures import ClientServerInfo, TraceValue
from slither_lsp.lsp.types.capabilities import ClientCapabilities, ServerCapabilities


class ServerContext:
    def __init__(self, server, server_capabilities=None):
        # Import some items late here
        import slither_lsp.lsp.servers.base_server as base_server

        # Create our basic LSP state variables
        self.server_initialized: bool = False
        self.client_initialized: bool = False
        self.shutdown: bool = False
        self.trace: TraceValue = TraceValue.OFF
        self.server: base_server.BaseServer = server
        self.client_info: Optional[ClientServerInfo] = None
        self.client_capabilities: ClientCapabilities = ClientCapabilities()
        self.server_capabilities: ServerCapabilities = server_capabilities or ServerCapabilities()

    @property
    def server_hooks(self):
        """
        Represents a set of hooks which can be used to fulfill requests.
        :return: Returns the server hook object used to fulfill requests.
        """
        return self.server.config.hooks

    @property
    def event_emitter(self):
        """
        Represents the main event emitter used by this server. This simply forwards to server.event_emitter.
        :return: Returns the main event emitter used by this server.
        """
        return self.server.event_emitter

    @property
    def server_info(self) -> ClientServerInfo:
        return ClientServerInfo(
            name='Slither Language Server',
            version=require("slither-lsp")[0].version
        )
