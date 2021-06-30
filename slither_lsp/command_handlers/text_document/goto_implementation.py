from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_params import TypeDefinitionParams, ImplementationParams


class GoToImplementationHandler(BaseCommandHandler):
    """
    Handler for the 'textDocument/implementation' request, which resolves a implementation location of a symbol at a
    given text document position.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_implementation
    """
    method_name = "textDocument/implementation"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/implementation' request and attempts to resolve a implementation location of a symbol
        at a given text document position.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_implementation
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: Location | Location[] | LocationLink[] | None
        """
        # Parse our params
        params: ImplementationParams = ImplementationParams.from_dict(params)

        # Define our result
        result = None

        # If we have a hook, call it
        if context.server_hooks is not None:
            result = context.server_hooks.goto_implementation(context, params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.implementation',
            params=params,
            result=result
        )

        return result
