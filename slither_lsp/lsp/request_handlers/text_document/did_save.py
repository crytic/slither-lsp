from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import DidSaveTextDocumentParams


class DidSaveHandler(BaseRequestHandler):
    """
    Handler for the 'textDocument/didSave' notification, which signals a text document was saved.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_didSave
    """
    method_name = "textDocument/didSave"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/didSave' notification, which signals a text document was saved.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_didSave
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: None
        """
        # Parse our params
        params: DidSaveTextDocumentParams = DidSaveTextDocumentParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.didSave',
            params=params
        )

        # This is a notification so we return nothing
        return None
