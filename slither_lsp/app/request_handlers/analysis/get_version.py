from typing import Any

from pkg_resources import require

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext


class GetVersion(BaseRequestHandler):
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
