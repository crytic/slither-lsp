from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_params import TypeDefinitionParams, ImplementationParams, ReferenceParams


class FindReferencesHandler(BaseCommandHandler):
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
        :param params: The parameters object provided with this command.
        :return: Location[] | null
        """
        # Parse our params
        params: ReferenceParams = ReferenceParams.from_dict(params)

        # Define our result
        result = None

        # TODO: Add an abstraction layer here which we can call to to obtain results.

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.references',
            params=params,
            result=result
        )

        return result
