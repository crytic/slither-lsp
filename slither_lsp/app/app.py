from importlib.metadata import version as pkg_version
from logging import Logger

import slither_lsp.app.types.params as slsp
from slither_lsp.app import request_handlers
from slither_lsp.app.slither_server import SlitherServer


def create_server(logger: Logger):
    version = f"v{pkg_version('slither-lsp')}"
    server = SlitherServer(logger.getChild("server"), "slither-lsp", version)

    server.feature(slsp.SLITHER_GET_DETECTOR_LIST)(request_handlers.get_detector_list)
    server.feature(slsp.SLITHER_GET_VERSION)(request_handlers.get_version)

    server.feature(slsp.CRYTIC_COMPILE_GET_COMMAND_LINE_ARGUMENTS)(
        request_handlers.get_command_line_args
    )

    return server
