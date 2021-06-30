from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.types.errors import LSPError, LSPErrorCode
from slither_lsp.lsp.state.server_context import ServerContext


class AnalysisDeleteHandler(BaseRequestHandler):
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
