from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import SetTraceParams


class SetTraceHandler(BaseRequestHandler):
    """
    Handler for the '$/setTrace' notification, which sets the verbosity level of log traces on the server.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#setTrace
    """
    method_name = "$/setTrace"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        # Parse our initialization params
        params: SetTraceParams = SetTraceParams.from_dict(params)

        # Set our value and emit a relevant event.
        context.trace = params.value
        context.event_emitter.emit('trace.set', context.trace)

        # Notifications do not return a response
        return None
