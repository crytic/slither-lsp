from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from typing import Any
from slither_lsp.state.server_context import ServerContext
from slither_lsp.errors.lsp_error import LSPError, LSPErrorCode


class AnalyzeHandler(BaseCommandHandler):
    """
    Handler which invokes slither analysis on a given target
    """
    method_name = "$/slither/analyze"

    @staticmethod
    def process(context: ServerContext, params: Any) -> Any:
        # TODO: Use context.register_analysis(...)
        raise LSPError(LSPErrorCode.InvalidParams, "ANALYSIS NOT YET IMPLEMENTED", None)
