import argparse

import logging

from slither_lsp.servers.console_server import ConsoleServer
from slither_lsp.servers.network_server import NetworkServer

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

    # Determine which server provider to use.
    if args.port:
        # Initialize a network server (using the provided host/port to communicate over TCP).
        server = NetworkServer(args.port)
    else:
        # Initialize a console server (uses stdio to communicate)
        server = ConsoleServer()

    # Begin processing command_handlers
    server.start()


if __name__ == "__main__":
    main()
