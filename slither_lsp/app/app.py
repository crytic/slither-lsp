from typing import Optional

from slither_lsp.app.app_hooks import SlitherLSPHooks
from slither_lsp.commands.workspace.get_workspace_folders import GetWorkspaceFoldersRequest
from slither_lsp.commands.window.log_message import LogMessageNotification
from slither_lsp.servers.base_server import BaseServer
from slither_lsp.servers.console_server import ConsoleServer
from slither_lsp.servers.network_server import NetworkServer
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import MessageType, Diagnostic, Range, Position, DiagnosticSeverity
from slither_lsp.types.lsp_capabilities import ServerCapabilities, WorkspaceServerCapabilities, \
    WorkspaceFoldersServerCapabilities
from slither_lsp.types.lsp_params import ShowDocumentParams, LogMessageParams, ShowMessageParams
from slither_lsp.commands.window.show_message import ShowMessageNotification
from slither_lsp.commands.window.show_document import ShowDocumentRequest
from slither_lsp.commands.text_document.publish_diagnostics import PublishDiagnosticsNotification, \
    PublishDiagnosticsParams


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
        Represents the initial server capabilities to start the server with.
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

    def start(self):
        """
        The main entry point for the application layer of slither-lsp.
        :return: None
        """

        # Create our hooks to fulfill LSP requests
        server_hooks = SlitherLSPHooks(self)

        # Determine which server provider to use.
        if self.port:
            # Initialize a network server (using the provided host/port to communicate over TCP).
            self.server = NetworkServer(
                self.port,
                server_capabilities=self.initial_server_capabilities,
                server_hooks=server_hooks
            )
        else:
            # Initialize a console server (uses stdio to communicate)
            self.server = ConsoleServer(
                server_capabilities=self.initial_server_capabilities,
                server_hooks=server_hooks
            )

        # Subscribe to our events
        self.server.event_emitter.on('client.initialized', self.on_client_initialized)

        # Begin processing command_handlers
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


