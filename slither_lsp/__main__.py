import argparse

import logging

from slither_lsp.servers.console_server import ConsoleServer
from slither_lsp.servers.network_server import NetworkServer
from slither_lsp.types.lsp_capabilities import ServerCapabilities, WorkspaceServerCapabilities, \
    WorkspaceFoldersServerCapabilities

logging.basicConfig()
logging.getLogger("slither_lsp").setLevel(logging.INFO)


def parse_args() -> argparse.Namespace:
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    # Initialize our argument parser
    parser = argparse.ArgumentParser(
        description="slither-lsp",
        usage="slither-lsp [options]",
    )

    # We want to offer a switch to communicate over a network socket rather than stdin/stdout.
    parser.add_argument(
        "--port",
        help="Indicates that the RPC server should use a TCP socket with the provided port, rather "
             "than stdio.",
        type=int
    )

    # TODO: Perform validation for port number

    return parser.parse_args()


def main() -> None:
    """
    The main entry point for the application. Parses arguments and starts the RPC server.
    :return: None
    """
    # Parse all arguments
    args = parse_args()

    # Create our capabilities object to determine what capabilities we want this application to have.
    server_capabilities: ServerCapabilities = ServerCapabilities(
        workspace=WorkspaceServerCapabilities(
            workspace_folders=WorkspaceFoldersServerCapabilities(
                supported=True,
                change_notifications=True
            )
        )
    )

    # Determine which server provider to use.
    if args.port:
        # Initialize a network server (using the provided host/port to communicate over TCP).
        server = NetworkServer(args.port, server_capabilities=server_capabilities)
    else:
        # Initialize a console server (uses stdio to communicate)
        server = ConsoleServer(server_capabilities=server_capabilities)

    # Begin processing command_handlers
    server.start()

    # TODO: Remove these tests.
    while not server.context or not server.context.client_initialized:
        pass
    from slither_lsp.commands.workspace.get_workspace_folders import GetWorkspaceFoldersRequest
    from slither_lsp.commands.window.log_message import LogMessageNotification
    from slither_lsp.types.lsp_basic_structures import MessageType, Diagnostic, Range, Position
    from slither_lsp.types.lsp_params import ShowDocumentParams, LogMessageParams, ShowMessageParams
    from slither_lsp.commands.window.show_message import ShowMessageNotification
    from slither_lsp.commands.window.show_document import ShowDocumentRequest
    from slither_lsp.commands.text_document.publish_diagnostics import PublishDiagnosticsNotification, \
        PublishDiagnosticsParams

    folders = GetWorkspaceFoldersRequest.send(server.context)
    LogMessageNotification.send(server.context, LogMessageParams(MessageType.WARNING, "TEST LOGGED MSG!"))
    ShowMessageNotification.send(server.context, ShowMessageParams(MessageType.ERROR, "TEST SHOWN MSG!"))
    shown_doc = ShowDocumentRequest.send(
        server.context,ShowDocumentParams(
            r'file:///C:/Users/X/Documents/GitHub/testcontracts/compact.ast',
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
                )
            ]
        )
    )
    f = folders


if __name__ == "__main__":
    main()
