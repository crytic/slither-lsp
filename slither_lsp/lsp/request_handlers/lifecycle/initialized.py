from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext


class InitializedHandler(BaseRequestHandler):
    """
    Handler for the 'initialized' notification, which notifies the server that the client successfully initialized.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#initialized
    """
    method_name = "initialized"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:

        # Set our context into an initialized state.
        context.client_initialized = True
        context.event_emitter.emit('client.initialized')

        # Notifications do not return a response
        return None
