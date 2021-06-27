from typing import Any, Optional

from slither_lsp.commands.base_command import BaseCommand
from slither_lsp.errors.lsp_errors import CapabilitiesNotSupportedError
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import MessageType, Range


class ShowDocumentRequest(BaseCommand):
    """
    Request which is sent to the client to display a particular document.
    """
    method_name = 'window/showDocument'

    @classmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
        client_supported: bool = context.client_capabilities.get(
            'window.showDocument.support',
            default=False,
            enforce_type=bool
        )
        return client_supported

    @classmethod
    def send(cls, context: ServerContext, uri: str, external: Optional[bool] = None, take_focus: Optional[bool] = None,
             selection: Optional[Range] = None) -> Any:
        """
        Sends a 'window/showDocument' request to the client.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-current/#window_showDocument
        :param context: The server context which determines the server to use to send the message.
        :param uri: The document uri to show.
        :param external: Indicates to show the resource in an external program. To show for example
        `https://code.visualstudio.com/` in the default WEB browser set `external` to `true`.
        :param take_focus: An optional property to indicate whether the editor showing the document should take focus
        or not. Clients might ignore this property if an external program is started.
        :param selection: An optional selection range if the document is a text document. Clients might ignore the
        property if an external program is started or the file is not a text file.
        :return: Returns a boolean indicating if the operation had succeeded.
        """

        # Throw an exception if we don't support the underlying capabilities.
        if not cls.has_capabilities(context):
            raise CapabilitiesNotSupportedError(cls)

        # Construct our request data
        request = {
            'uri': uri
        }
        if external is not None:
            request['external'] = external
        if take_focus is not None:
            request['takeFocus'] = take_focus
        if selection is not None:
            request['selection'] = selection.to_dict()

        # Send the created notification.
        response: dict = context.server.send_request_message(cls.method_name, request)

        # Our response should contain a 'success' boolean. Otherwise we'll signal a failure.
        if isinstance(response, dict):
            success = response.get('success')
            if isinstance(success, bool):
                return success

        return False
