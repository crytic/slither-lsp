from importlib.metadata import version as pkg_version
from logging import Logger

import slither_lsp.app.request_handlers as request_handlers
from slither_lsp.app.slither_server import SlitherServer


def create_server(logger: Logger):
    version = f"v{pkg_version('slither-lsp')}"
    server = SlitherServer(logger.getChild("server"), "slither-lsp", version)

    server.feature("$/slither/getDetectorList")(request_handlers.get_detector_list)
    server.feature("$/slither/getVersion")(request_handlers.get_version)

    server.feature("$/cryticCompile/solcStandardJson/autogenerate")(
        request_handlers.autogenerate_standard_json
    )
    server.feature("$/cryticCompile/getCommandLineArguments")(
        request_handlers.get_command_line_args
    )

    return server
