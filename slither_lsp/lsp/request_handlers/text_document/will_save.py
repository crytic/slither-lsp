from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import DidChangeTextDocumentParams, WillSaveTextDocumentParams


class WillSaveHandler(BaseRequestHandler):
    """
    Handler for the 'textDocument/willSave' notification, which signals a text document is about to be saved.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_willSave
    """
    method_name = "textDocument/willSave"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/willSave' notification, which signals a text document is about to be saved.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_willSave
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: None
        """
        # Parse our params
        params: WillSaveTextDocumentParams = WillSaveTextDocumentParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.willSave',
            params=params
        )

        # This is a notification so we return nothing
        return None
