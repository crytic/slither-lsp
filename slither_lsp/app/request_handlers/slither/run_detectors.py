from typing import Any

from slither.__main__ import get_detectors_and_printers, _process as process_detectors_and_printers

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.types.errors import LSPError, LSPErrorCode
from slither_lsp.lsp.state.server_context import ServerContext


class RunDetectorsHandler(BaseRequestHandler):
    """
    Handler which runs slither detectors and returns relevant detector results.
    """
    method_name = "$/slither/runDetectors"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        # Verify we were provided an analysisId
        if 'analysisId' not in params:
            raise LSPError(
                LSPErrorCode.InvalidParams,
                "'analysisId' key was not provided to run detectors.'",
                None
            )

        # Obtain our analysis id and relevant slither instance
        analysis_id = params['analysisId']
        slither = context.get_analysis(analysis_id)

        # Run detectors
        detector_classes, _ = get_detectors_and_printers()
        _, detector_results, _, _ = process_detectors_and_printers(slither, detector_classes, [])
        return detector_results
