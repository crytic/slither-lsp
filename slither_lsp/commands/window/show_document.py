from typing import Any, Optional

from slither_lsp.commands.base_command import BaseCommand
from slither_lsp.errors.lsp_errors import CapabilitiesNotSupportedError
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import MessageType, Range
from slither_lsp.types.lsp_capabilities import ShowDocumentClientCapabilities
from slither_lsp.types.lsp_params import ShowDocumentParams, ShowDocumentResult


class ShowDocumentRequest(BaseCommand):
    """
    Request which is sent to the client to display a particular document.
    """
    method_name = 'window/showDocument'

    @classmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
        # Attempt to obtain our client capabilities
        client_supported: Optional[dict] = context.client_capabilities.get(
            'window.showDocument',
            default=None,
            enforce_type=dict
        )

        # If we obtained capabilities, parse them and return our status, otherwise indicate we do not support these
        # capabilities.
        if client_supported is not None:
            return ShowDocumentClientCapabilities.from_dict(client_supported).support
        return False

    @classmethod
    def send(cls, context: ServerContext, params: ShowDocumentParams) -> Any:
        """
        Sends a 'window/showDocument' request to the client.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-current/#window_showDocument
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters needed to send the request.
        """

        # Throw an exception if we don't support the underlying capabilities.
        if not cls.has_capabilities(context):
            raise CapabilitiesNotSupportedError(cls)

        # Send the created notification.
        response: dict = context.server.send_request_message(cls.method_name, params.to_dict())
        response: ShowDocumentResult = ShowDocumentResult.from_dict(response)

        # Return our result
        return response.success
