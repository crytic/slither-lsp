from slither_lsp.commands.base_command import BaseCommand
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_params import ShowMessageParams


class ShowMessageNotification(BaseCommand):
    """
    Notification which is sent to the client to show a message.
    """
    method_name = 'window/showMessage'

    @classmethod
    def send(cls, context: ServerContext, params: ShowMessageParams) -> None:
        """
        Sends a 'window/showMessage' notification to the client.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_showMessage
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters needed to send the request.
        :return: None
        """
        context.server.send_notification_message(cls.method_name, params.to_dict())
