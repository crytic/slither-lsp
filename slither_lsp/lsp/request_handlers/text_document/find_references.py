from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import ReferenceParams


class FindReferencesHandler(BaseRequestHandler):
    """
    Handler for the 'textDocument/references' request, which resolves project-wide references for the symbol denoted
    by the given text document position.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_references
    """
    method_name = "textDocument/references"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/references' request, which resolves project-wide references for the symbol denoted
        by the given text document position.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_references
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: Location[] | None
        """
        # Parse our params
        params: ReferenceParams = ReferenceParams.from_dict(params)

        # Define our result
        result = None

        # If we have a hook, call it
        if context.server_hooks is not None:
            result = context.server_hooks.find_references(context, params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.references',
            params=params,
            result=result
        )

        return result
