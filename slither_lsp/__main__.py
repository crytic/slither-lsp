import argparse
import logging

from slither_lsp.app.app import create_server


def _parse_loglevel(value: str) -> int:
    return getattr(logging, value.upper())


def _parse_args() -> argparse.Namespace:
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    # Initialize our argument parser
    parser = argparse.ArgumentParser(
        description="slither-lsp",
    )
    parser.add_argument("--loglevel", type=_parse_loglevel, default="WARNING")
    subcommands = parser.add_subparsers(dest="mode")
    tcp = subcommands.add_parser(
        "tcp", help="Starts a TCP server instead of communicating over STDIO"
    )
    ws = subcommands.add_parser(
        "websocket",
        help="Starts a WebSocket server instead of communicating over STDIO",
    )

    tcp.add_argument(
        "--port",
        help="The port the TCP server should be listening.",
        type=int,
        default=12345,
    )
    tcp.add_argument(
        "--host",
        help="The host the TCP server should be listening on.",
        type=str,
        default="127.0.0.1",
    )

    ws.add_argument(
        "--port",
        help="The port the WebSocket server should be listening.",
        type=int,
        default=12345,
    )
    ws.add_argument(
        "--host",
        help="The host the WebSocket server should be listening on.",
        type=str,
        default="127.0.0.1",
    )

    # TODO: Perform validation for port number

    return parser.parse_args()


def main() -> None:
    """
    The main entry point for the application. Parses arguments and starts the RPC server.
    :return: None
    """
    # Parse all arguments
    args = _parse_args()
    logger = logging.getLogger("slither_lsp")
    logger.setLevel(args.loglevel)

    app = create_server(logger)

    # Run our main app
    if args.mode == "tcp":
        app.start_tcp(args.host, args.port)
    elif args.mode == "ws":
        app.start_ws(args.host, args.port)
    else:
        app.start_io()


if __name__ == "__main__":
    main()
