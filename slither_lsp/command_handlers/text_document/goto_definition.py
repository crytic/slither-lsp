from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_params import DefinitionParams


class GoToDefinitionHandler(BaseCommandHandler):
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
        :param params: The parameters object provided with this command.
        :return: Location | Location[] | LocationLink[] | null
        """
        # Parse our initialization params
        params: DefinitionParams = DefinitionParams.from_dict(params)

        # Define our result
        result = None

        # TODO: Add an abstraction layer here which we can call to to obtain results.

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.definition',
            params=params,
            result=result
        )

        return result
