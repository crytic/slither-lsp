from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import TraceValue


class SetTraceHandler(BaseCommandHandler):
    """
    Handler for the '$/setTrace' notification, which sets the verbosity level of log traces on the server.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#setTrace
    """
    method_name = "$/setTrace"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:

        # Parse trace level
        trace_level = params.get('value')
        if trace_level is not None and isinstance(trace_level, str):
            context.trace = TraceValue(trace_level)
            context.event_emitter.emit('trace.set', context.trace)

        # Notifications do not return a response
        return None
