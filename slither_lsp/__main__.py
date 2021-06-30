import argparse

import logging

from slither_lsp.app.app import SlitherLSPApp
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

    # Run our main app
    app = SlitherLSPApp(port=args.port)
    app.start()


if __name__ == "__main__":
    main()
