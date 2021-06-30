from typing import Dict, List, Optional

from pkg_resources import require
from slither import Slither

from slither_lsp.lsp.types.capabilities import ClientCapabilities, ServerCapabilities
from slither_lsp.lsp.types.basic_structures import WorkspaceFolder, ClientServerInfo, TraceValue


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
        self.workspace_folders: List[WorkspaceFolder] = []

        # Create our analysis results structure
        self._analysis_results: Dict[int, Slither] = {}
        self._next_analysis_id: int = 0

    @property
    def server_hooks(self):
        """
        Represents a set of hooks which can be used to fulfill requests.
        :return: Returns the server hook object used to fulfill requests.
        """
        return self.server.server_hooks

    @property
    def event_emitter(self):
        """
        Represents the main event emitter used by this server. This simply forwards to server.event_emitter.
        :return: Returns the main event emitter used by this server.
        """
        return self.server.event_emitter

    def register_analysis(self, slither_instance: Slither) -> int:
        """
        Registers an analysis object with a unique identifier for subsequent operations to be performed on.
        :param slither_instance: The slither analysis instance which we wish to store for subsequent operations to be
        performed on.
        :return: Returns a key which can be used to obtain
        """
        # Obtain our next analysis id
        analysis_id = self._next_analysis_id
        self._next_analysis_id += 1

        # Set our slither instance in our lookup and return the analysis id.
        self._analysis_results[analysis_id] = slither_instance
        return analysis_id

    def unregister_analysis(self, analysis_id: int) -> None:
        """
        Unregisters an analysis object associated with a unique key from a previous registration.
        :param analysis_id: The unique key associated with a previously registered analysis.
        :return: None
        """
        self._analysis_results.pop(analysis_id, None)

    def get_analysis(self, analysis_id: int) -> Optional[Slither]:
        """
        Obtains an analysis object associated with a unique key during a previous registration.
        :param analysis_id: The unique key associated with a previously registered analysis.
        :return: Returns a Slither object if one exists with this key, otherwise None.
        """
        return self._analysis_results.get(analysis_id, None)

    @property
    def server_info(self) -> ClientServerInfo:
        return ClientServerInfo(
            name='Slither Language Server',
            version=require("slither-lsp")[0].version
        )
