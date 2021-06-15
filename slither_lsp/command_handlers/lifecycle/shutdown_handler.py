from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from typing import Any
from slither_lsp.state.server_context import ServerContext


class ShutdownHandler(BaseCommandHandler):
    """
    Handler for the 'shutdown' request, which prepares the server for a subsequent exit.
    Reference: https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#shutdown
    """
    method_name = "shutdown"

    @staticmethod
    def process(context: ServerContext, params: Any) -> Any:
        # Set the server context into a shutdown state, so it should not process anything heavily.
        # TODO: Create and trigger an event for this + ensure other code uses this state to not perform any meaningful
        #  updates.
        context.shutdown = True

        # The return value on success is null.
        return None
