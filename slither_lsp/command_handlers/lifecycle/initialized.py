from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext


class InitializedHandler(BaseCommandHandler):
    """
    Handler for the 'initialized' notification, which notifies the server that the client successfully initialized.
    Reference: https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#initialized
    """
    method_name = "initialized"

    @staticmethod
    def process(context: ServerContext, params: Any) -> Any:

        # Set our context into an initialized state.
        # TODO: Create and trigger an event for this.
        context.client_initialized = True

        # Notifications do not return a response
        return None
