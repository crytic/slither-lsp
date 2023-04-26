from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure
from slither_lsp.lsp.types.params import ImplementationParams


class GoToImplementationHandler(BaseRequestHandler):
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
        :param params: The parameters object provided with this message.
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

        # Serialize our result depending on the type.
        if result is not None:
            if isinstance(result, SerializableStructure):
                result = result.to_dict()
            elif isinstance(result, list):
                result = [
                    result_element.to_dict() if isinstance(result_element, SerializableStructure) else result_element
                    for result_element in result
                ]

        return result