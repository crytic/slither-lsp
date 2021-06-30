from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.types.lsp_errors import LSPError, LSPErrorCode
from slither_lsp.state.server_context import ServerContext


class AnalysisDeleteHandler(BaseCommandHandler):
    """
    Handler which frees a previously created analysis.
    """
    method_name = "$/slither/analysis/delete"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:

        # Verify we were provided an analysisId
        if 'analysisId' not in params:
            raise LSPError(
                LSPErrorCode.InvalidParams,
                "'analysisId' key was not provided for deletion of analysis.'",
                None
            )

        # Obtain our analysis id
        analysis_id = params['analysisId']

        # Unregister the analysis
        context.unregister_analysis(analysis_id)
        return None
