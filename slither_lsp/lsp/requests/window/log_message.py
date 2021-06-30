from slither_lsp.lsp.requests.base_request import BaseRequest
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import LogMessageParams


class LogMessageNotification(BaseRequest):
    """
    Notification which is sent to the client to show a message.
    """
    method_name = 'window/logMessage'

    @classmethod
    def send(cls, context: ServerContext, params: LogMessageParams) -> None:
        """
        Sends a 'window/logMessage' notification to the client.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_logMessage
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters needed to send the request.
        :return: None
        """
        context.server.send_notification_message(cls.method_name, params.to_dict())