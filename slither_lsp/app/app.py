import inspect
from typing import Optional, Type, List

from slither_lsp.app.app_hooks import SlitherLSPHooks
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
    WorkspaceFoldersServerCapabilities
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

    @property
    def context(self) -> ServerContext:
        """
        An alias for the ServerContext object used by the server.
        :return: Returns the ServerContext object used by the server.
        """
        return self.server.context

    @property
    def initial_server_capabilities(self) -> ServerCapabilities:
        """
        Represents the initial server capabilities to start the server with. This signals to the client which
        capabilities they can expect to leverage.
        :return: Returns the server capabilities to be used with the server.
        """
        return ServerCapabilities(
            declaration_provider=True,
            definition_provider=True,
            type_definition_provider=True,
            implementation_provider=True,
            references_provider=True,
            workspace=WorkspaceServerCapabilities(
                workspace_folders=WorkspaceFoldersServerCapabilities(
                    supported=True,
                    change_notifications=True
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

        # Begin processing request_handlers
        self.server.start()

    def on_client_initialized(self):
        # TODO: Move main loop logic to kick off from here.
        folders = GetWorkspaceFoldersRequest.send(self.context)
        LogMessageNotification.send(self.context,
                                    LogMessageParams(type=MessageType.WARNING, message="TEST LOGGED MSG!"))
        ShowMessageNotification.send(self.context,
                                     ShowMessageParams(type=MessageType.ERROR, message="TEST SHOWN MSG!"))
        shown_doc = ShowDocumentRequest.send(
            self.context,
            ShowDocumentParams(
                uri=r'file:///C:/Users/X/Documents/GitHub/testcontracts/compact.ast',
                take_focus=True, external=None, selection=None
            )
        )
        PublishDiagnosticsNotification.send(
            self.context,
            PublishDiagnosticsParams(
                uri="TEST.BLAH",
                version=None,
                diagnostics=[
                    Diagnostic(
                        message="test diagnostic message",
                        range=Range(Position(0, 0), Position(0, 0)),
                        severity=DiagnosticSeverity.ERROR
                    )
                ]
            )
        )
        f = folders


