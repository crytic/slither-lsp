from logging import Handler, LogRecord, FATAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from pygls.server import LanguageServer
from lsprotocol.types import MessageType

_level_to_type = {
    FATAL: MessageType.Error,
    ERROR: MessageType.Error,
    WARNING: MessageType.Warning,
    INFO: MessageType.Info,
    DEBUG: MessageType.Debug,
    NOTSET: MessageType.Debug,
}


class LSPHandler(Handler):
    """
    Forwards log messages to the LSP client
    """

    def __init__(self, server: LanguageServer):
        Handler.__init__(self)
        self.server = server

    def emit(self, record: LogRecord):
        msg = self.format(record)
        msg_type = _level_to_type[record.levelno]
        self.server.show_message_log(msg, msg_type=msg_type)
