from typing import Any

from slither.__main__ import get_detectors_and_printers, output_detectors_json

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext


class GetDetectorListHandler(BaseCommandHandler):
    """
    Handler which invokes slither to obtain a list of all detectors and some properties that describe them.
    """
    method_name = "$/slither/getDetectorList"

    @staticmethod
    def process(context: ServerContext, params: Any) -> Any:
        # Obtain a list of detectors
        detectors, _ = get_detectors_and_printers()

        # Obtain the relevant object to be output as JSON.
        detector_types_json = output_detectors_json(detectors)
        return detector_types_json
