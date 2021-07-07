from typing import Any

from slither_lsp.app.types.params import SetCompilationTargetsParams
from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext


class SetCompilationTargetsHandler(BaseRequestHandler):
    """
    Handler which sets compilation targets for the language server. If empty, auto-compilation is used instead.
    """
    method_name = "$/compilation/setCompilationTargets"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        # Validate the structure of our request
        params: SetCompilationTargetsParams = SetCompilationTargetsParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'compilation.setCompilationTargets',
            params=params
        )

        # This returns nothing on success.
        return None
