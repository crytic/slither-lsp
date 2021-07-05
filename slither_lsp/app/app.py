import inspect
from threading import Lock
from typing import Optional, Type, List, Tuple

from crytic_compile import CryticCompile, InvalidCompilation
from crytic_compile.platform.solc_standard_json import SolcStandardJson
from slither import Slither

from slither_lsp.app.app_hooks import SlitherLSPHooks
from slither_lsp.app.solidity_workspace import SolidityWorkspace
from slither_lsp.app.types.analysis_structures import AnalysisResult
from slither_lsp.app.types.compilation_structures import CompilationTarget, CompilationTargetType
from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.requests.workspace.get_workspace_folders import GetWorkspaceFoldersRequest
from slither_lsp.lsp.requests.window.log_message import LogMessageNotification
from slither_lsp.lsp.servers.base_server import BaseServer
from slither_lsp.lsp.servers.console_server import ConsoleServer
from slither_lsp.lsp.servers.network_server import NetworkServer
from slither_lsp.lsp.state.server_config import ServerConfig
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.basic_structures import MessageType, Diagnostic, Range, Position, DiagnosticSeverity
from slither_lsp.lsp.types.capabilities import ServerCapabilities, WorkspaceServerCapabilities, \
    WorkspaceFoldersServerCapabilities, TextDocumentSyncOptions, TextDocumentSyncKind, SaveOptions, \
    WorkspaceFileOperationsServerCapabilities, FileOperationRegistrationOptions, FileOperationFilter, \
    FileOperationPattern, FileOperationPatternKind, FileOperationPatternOptions
from slither_lsp.lsp.types.params import ShowDocumentParams, LogMessageParams, ShowMessageParams
from slither_lsp.lsp.requests.window.show_message import ShowMessageNotification
from slither_lsp.lsp.requests.window.show_document import ShowDocumentRequest
from slither_lsp.lsp.requests.text_document.publish_diagnostics import PublishDiagnosticsNotification, \
    PublishDiagnosticsParams
from slither_lsp.app.request_handlers import registered_handlers


class SlitherLSPApp:
    def __init__(self, port: Optional[int]):
        self.port: Optional[int] = port
        self.server: Optional[BaseServer] = None
        self.solidity_workspace: Optional[SolidityWorkspace] = None

    @property
    def initial_server_capabilities(self) -> ServerCapabilities:
        """
        Represents the initial server capabilities to start the server with. This signals to the client which
        capabilities they can expect to leverage.
        :return: Returns the server capabilities to be used with the server.
        """
        # Create our file operation registration options to know which files to watch.
        file_operation_registration_options = FileOperationRegistrationOptions([
            FileOperationFilter(
                scheme='file',
                pattern=FileOperationPattern(
                    glob='**/*.sol',
                    matches=FileOperationPatternKind.FILE,
                    options=FileOperationPatternOptions(
                        ignore_case=True
                    )
                )
            )
        ])

        # Constructor our overall capabilities object.
        return ServerCapabilities(
            text_document_sync=TextDocumentSyncOptions(
                open_close=True,
                change=TextDocumentSyncKind.FULL,
                will_save=True,
                will_save_wait_until=False,
                save=SaveOptions(
                    include_text=True
                )
            ),
            declaration_provider=True,
            definition_provider=True,
            type_definition_provider=True,
            implementation_provider=True,
            references_provider=True,
            workspace=WorkspaceServerCapabilities(
                workspace_folders=WorkspaceFoldersServerCapabilities(
                    supported=True,
                    change_notifications=True
                ),
                file_operations=WorkspaceFileOperationsServerCapabilities(
                    did_create=file_operation_registration_options,
                    will_create=file_operation_registration_options,
                    did_rename=file_operation_registration_options,
                    will_rename=file_operation_registration_options,
                    did_delete=file_operation_registration_options,
                    will_delete=file_operation_registration_options
                )
            )
        )

    @staticmethod
    def _get_additional_request_handlers() -> List[Type[BaseRequestHandler]]:
        # Obtain all additional request handler types imported in our registered list and put them in an array
        additional_request_handlers: list = []
        for ch in [getattr(registered_handlers, name) for name in dir(registered_handlers)]:
            if inspect.isclass(ch) and ch != BaseRequestHandler and issubclass(ch, BaseRequestHandler):
                additional_request_handlers.append(ch)

        return additional_request_handlers

    def start(self):
        """
        The main entry point for the application layer of slither-lsp.
        :return: None
        """

        # Create our hooks to fulfill LSP requests
        server_hooks = SlitherLSPHooks(self)

        # Create our server configuration with our application hooks
        server_config = ServerConfig(
            initial_server_capabilities=self.initial_server_capabilities,
            hooks=server_hooks,
            additional_request_handlers=self._get_additional_request_handlers()
        )

        # Determine which server provider to use.
        if self.port:
            # Initialize a network server (using the provided host/port to communicate over TCP).
            self.server = NetworkServer(self.port, server_config=server_config)
        else:
            # Initialize a console server (uses stdio to communicate)
            self.server = ConsoleServer(server_config=server_config)

        # Subscribe to our events
        self.server.event_emitter.on('client.initialized', self.on_client_initialized)

        # Create our solidity workspace so it can register relevant events
        self.solidity_workspace = SolidityWorkspace(self)

        # Begin processing request_handlers
        self.server.start()

    def on_client_initialized(self):
        # TODO: Move main loop logic to kick off from here.
        folders = GetWorkspaceFoldersRequest.send(self.server.context)
        LogMessageNotification.send(self.server.context,
                                    LogMessageParams(type=MessageType.WARNING, message="TEST LOGGED MSG!"))
        ShowMessageNotification.send(self.server.context,
                                     ShowMessageParams(type=MessageType.ERROR, message="TEST SHOWN MSG!"))
        shown_doc = ShowDocumentRequest.send(
            self.server.context,
            ShowDocumentParams(
                uri=r'file:///C:/Users/X/Documents/GitHub/testcontracts/compact.ast',
                take_focus=True, external=None, selection=None
            )
        )
        PublishDiagnosticsNotification.send(
            context=self.server.context,
            params=PublishDiagnosticsParams(
                uri="TEST.BLAH",
                version=None,
                diagnostics=[
                    Diagnostic(
                        message="test diagnostic message",
                        range=Range(
                            start=Position(0, 0),
                            end=Position(0, 0)
                        ),
                        severity=DiagnosticSeverity.ERROR
                    )
                ]
            )
        )
        f = folders
