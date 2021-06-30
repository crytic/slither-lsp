from slither_lsp.lsp.requests.base_request import BaseRequest
from slither_lsp.lsp.types.errors import CapabilitiesNotSupportedError
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import PublishDiagnosticsParams


class PublishDiagnosticsNotification(BaseRequest):
    """
    Notification which sends diagnostics to the client to display.
    """

    method_name = "textDocument/publishDiagnostics"

    @classmethod
    def _check_capabilities(cls, context: ServerContext) -> None:
        """
        Checks if the client has capabilities for this message. Throws a CapabilitiesNotSupportedError if it does not.
        :param context: The server context which tracks state for the server.
        :return: None
        """
        # Check if we have basic capabilities for this.
        supported = context.client_capabilities.text_document and \
        context.client_capabilities.text_document.publish_diagnostics
        if not supported:
            raise CapabilitiesNotSupportedError(cls)

    @classmethod
    def send(cls, context: ServerContext, params: PublishDiagnosticsParams) -> None:
        """
        Sends a 'textDocument/publishDiagnostics' request to the client to obtain workspace folders.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_showMessage
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters needed to send the request.
        :return: None
        """

        # Invoke the operation otherwise.
        context.server.send_notification_message(cls.method_name, params.to_dict())
