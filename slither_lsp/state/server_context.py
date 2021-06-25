from typing import Callable, Dict, List, Optional

from slither import Slither

from slither_lsp.types.server_enums import TraceValue
from slither_lsp.types.workspace_types import WorkspaceFolder, ClientInfo


class ServerContext:
    def __init__(self, server):
        # Import late here to avoid circular reference issues.
        import slither_lsp.servers.base_server as base_server

        # Create our basic LSP state variables
        self._server_initialized: bool = False
        self._client_initialized: bool = False
        self.shutdown: bool = False
        self.trace: TraceValue = TraceValue.OFF
        self.server: base_server.BaseServer = server
        self.client_info: Optional[ClientInfo] = None
        self.client_capabilities: dict = {}
        self.workspace_folders: List[WorkspaceFolder] = []

        # Create our main events
        self.on_server_initialized: Optional[Callable[[], None]] = None
        self.on_client_initialized: Optional[Callable[[], None]] = None

        # Create our analysis results structure
        self._analysis_results: Dict[int, Slither] = {}
        self._next_analysis_id: int = 0

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
    def server_initialized(self) -> bool:
        return self._server_initialized

    @server_initialized.setter
    def server_initialized(self, value: bool) -> None:
        # Set our initialized property and trigger the relevant event
        self._server_initialized = value
        if value and self.on_server_initialized is not None:
            self.on_server_initialized()

    @property
    def client_initialized(self) -> bool:
        return self._client_initialized

    @client_initialized.setter
    def client_initialized(self, value: bool) -> None:
        # Set our initialized property and trigger the relevant event
        self._client_initialized = value
        if value and self.on_client_initialized is not None:
            self.on_client_initialized()
