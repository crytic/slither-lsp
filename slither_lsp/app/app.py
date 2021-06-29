from slither_lsp.commands.workspace.get_workspace_folders import GetWorkspaceFoldersRequest
from slither_lsp.commands.window.log_message import LogMessageNotification
from slither_lsp.servers.base_server import BaseServer
from slither_lsp.types.lsp_basic_structures import MessageType, Diagnostic, Range, Position, DiagnosticSeverity
from slither_lsp.types.lsp_params import ShowDocumentParams, LogMessageParams, ShowMessageParams
from slither_lsp.commands.window.show_message import ShowMessageNotification
from slither_lsp.commands.window.show_document import ShowDocumentRequest
from slither_lsp.commands.text_document.publish_diagnostics import PublishDiagnosticsNotification, \
    PublishDiagnosticsParams


class SlitherLSPApp:
    @staticmethod
    def run(server: BaseServer):
        """
        The main entry point for the application layer of slither-lsp.
        :return: None
        """
        # TODO: Remove these tests.
        while not server.context or not server.context.client_initialized:
            pass

        folders = GetWorkspaceFoldersRequest.send(server.context)
        LogMessageNotification.send(server.context,
                                    LogMessageParams(type=MessageType.WARNING, message="TEST LOGGED MSG!"))
        ShowMessageNotification.send(server.context,
                                     ShowMessageParams(type=MessageType.ERROR, message="TEST SHOWN MSG!"))
        shown_doc = ShowDocumentRequest.send(
            server.context,
            ShowDocumentParams(
                uri=r'file:///C:/Users/X/Documents/GitHub/testcontracts/compact.ast',
                take_focus=True, external=None, selection=None
            )
        )
        PublishDiagnosticsNotification.send(
            server.context,
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
