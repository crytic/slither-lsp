from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import DidOpenTextDocumentParams


class DidOpenHandler(BaseRequestHandler):
    """
    Handler for the 'textDocument/didOpen' notification, which signals newly opened text documents.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_didOpen
    """
    method_name = "textDocument/didOpen"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/didOpen' notification, which signals newly opened text documents.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_didOpen
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: None
        """
        # Parse our params
        params: DidOpenTextDocumentParams = DidOpenTextDocumentParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.didOpen',
            params=params
        )

        # This is a notification so we return nothing
        return None
