from typing import Any, Optional

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure
from slither_lsp.lsp.types.params import DeclarationParams, HoverParams, Hover


class HoverHandler(BaseRequestHandler):
    """
    Handler for the 'textDocument/hover' request, which resolves hover information at a given text document position.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_hover
    """
    method_name = "textDocument/hover"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/hover' request, which resolves hover information at a given text document position.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_hover
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: Hover | None
        """
        # Parse our params
        params: HoverParams = HoverParams.from_dict(params)

        # Define our result
        result = None

        # If we have a hook, call it
        if context.server_hooks is not None:
            result = context.server_hooks.hover(context, params)

        # Emit relevant events
        context.event_emitter.emit(
            'textDocument.hover',
            params=params,
            result=result
        )

        # Serialize our result depending on the type.
        if result is not None:
            if isinstance(result, SerializableStructure):
                result = result.to_dict()

        return result
