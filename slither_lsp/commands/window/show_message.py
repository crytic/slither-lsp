from typing import Any

from slither_lsp.commands.base_command import BaseCommand
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import MessageType


class ShowMessageNotification(BaseCommand):
    """
    Notification which is sent to the client to show a message.
    """
    method_name = 'window/showMessage'

    @classmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
        return True

    @classmethod
    def send(cls, context: ServerContext, message_type: MessageType, message: str) -> None:
        """
        Sends a 'window/showMessage' notification to the client.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_showMessage
        :param context: The server context which determines the server to use to send the message.
        :param message_type: The severity/level of the message to show.
        :param message: The message the client should log.
        :return: None
        """
        context.server.send_notification_message(
            cls.method_name,
            {
                'type': int(message_type),
                'message': message
            }
        )
