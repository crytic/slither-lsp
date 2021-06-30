from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import DefinitionParams


class GoToDefinitionHandler(BaseRequestHandler):
    """
    Handler for the 'textDocument/definition' request, which resolves a definition location of a symbol at a
    given text document position.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_definition
    """
    method_name = "textDocument/definition"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/definition' request and attempts to resolve a definition location of a symbol at a
        given text document position.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_definition
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: Location | Location[] | LocationLink[] | None
        """
        # Parse our params
        params: DefinitionParams = DefinitionParams.from_dict(params)

        # Define our result
        result = None

        # If we have a hook, call it
        if context.config.server_hooks is not None:
            result = context.config.server_hooks.goto_definition(context, params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.definition',
            params=params,
            result=result
        )

        return result
