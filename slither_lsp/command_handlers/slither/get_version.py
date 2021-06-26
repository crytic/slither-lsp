from typing import Any

from pkg_resources import require

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext


class GetVersion(BaseCommandHandler):
    """
    Handler which retrieves versions for slither, crytic-compile, and related applications.
    """
    method_name = "$/slither/getVersion"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        return {
            "slither": require("slither-analyzer")[0].version,
            "crytic_compile": require("crytic-compile")[0].version,
            "slither_lsp": require("slither-lsp")[0].version
        }
