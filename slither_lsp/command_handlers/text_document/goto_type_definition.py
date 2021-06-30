from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_params import TypeDefinitionParams


class GoToTypeDefinitionHandler(BaseCommandHandler):
    """
    Handler for the 'textDocument/typeDefinition' request, which resolves a type definition location of a symbol at a
    given text document position.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_typeDefinition
    """
    method_name = "textDocument/typeDefinition"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/typeDefinition' request and attempts to resolve a type definition location of a symbol
        at a given text document position.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_typeDefinition
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: Location | Location[] | LocationLink[] | None
        """
        # Parse our params
        params: TypeDefinitionParams = TypeDefinitionParams.from_dict(params)

        # Define our result
        result = None

        # If we have a hook, call it
        if context.server_hooks is not None:
            result = context.server_hooks.goto_type_definition(context, params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.typeDefinition',
            params=params,
            result=result
        )

        return result
