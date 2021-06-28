from typing import Any

from slither_lsp.commands.base_command import BaseCommand
from slither_lsp.errors.lsp_errors import CapabilitiesNotSupportedError
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_params import ShowDocumentParams, ShowDocumentResult


class ShowDocumentRequest(BaseCommand):
    """
    Request which is sent to the client to display a particular document.
    """
    method_name = 'window/showDocument'

    @classmethod
    def _check_capabilities(cls, context: ServerContext) -> None:
        """
        Checks if the client has capabilities for this command. Throws a CapabilitiesNotSupportedError if it does not.
        :param context: The server context which tracks state for the server.
        :return: None
        """
        if not context.client_capabilities.window and context.client_capabilities.window.show_document and \
                context.client_capabilities.window.show_document.support:
            raise CapabilitiesNotSupportedError(cls)

    @classmethod
    def send(cls, context: ServerContext, params: ShowDocumentParams) -> Any:
        """
        Sends a 'window/showDocument' request to the client.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-current/#window_showDocument
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters needed to send the request.
        """

        # Verify we have appropriate capabilities.
        cls._check_capabilities(context)

        # Send the created notification.
        response: dict = context.server.send_request_message(cls.method_name, params.to_dict())
        response: ShowDocumentResult = ShowDocumentResult.from_dict(response)

        # Return our result
        return response.success
