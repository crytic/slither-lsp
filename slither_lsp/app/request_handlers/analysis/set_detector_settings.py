from typing import Any

from slither_lsp.app.types.analysis_structures import SlitherDetectorSettings
from slither_lsp.app.types.params import SetCompilationTargetsParams
from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext


class SetDetectorSettingsHandler(BaseRequestHandler):
    """
    Handler which sets slither detector settings for the server. This manages how/if detector output is presented.
    """
    method_name = "$/slither/setDetectorSettings"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        # Validate the structure of our request
        params: SlitherDetectorSettings = SlitherDetectorSettings.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'slither.setDetectorSettings',
            params=params
        )

        # This returns nothing on success.
        return None
