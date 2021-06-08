from slither_lsp.types.server_enums import MessageType
from slither_lsp.state.server_context import ServerContext


def send_log_message_notification(context: ServerContext, message_type: MessageType, message: str) -> None:
    """
    Sends a 'window/logMessage' notification to the client.
    Reference: https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_logMessage
    :param context: The server context which determines the server to use to send the message.
    :param message_type: The severity/level of the message to log.
    :param message: The message the client should log.
    :return: None
    """
    context.server.send_notification_message(
        'window/logMessage',
        {
            'type': int(message_type),
            'message': message
        }
    )
