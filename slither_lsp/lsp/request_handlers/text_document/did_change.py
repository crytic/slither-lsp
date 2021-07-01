from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import DidChangeTextDocumentParams


class DidChangeHandler(BaseRequestHandler):
    """
    Handler for the 'textDocument/didChange' notification, which signals changes made to text documents.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_didChange
    """
    method_name = "textDocument/didChange"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/didChange' notification, which signals changes made to text documents.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_didChange
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: None
        """
        # Parse our params
        params: DidChangeTextDocumentParams = DidChangeTextDocumentParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.didChange',
            params=params
        )

        # This is a notification so we return nothing
        return None
