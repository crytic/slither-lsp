from enum import Enum, IntEnum


class MessageType(IntEnum):
    """
    Defines the severity level of a message to be shown/logged.
    """
    ERROR = 1
    WARNING = 2
    INFO = 3
    LOG = 4


class TraceValue(Enum):
    """
    Defines the level of verbosity to trace server actions with.
    """
    OFF = 'off'
    MESSAGES = 'messages'
    VERBOSE = 'verbose'
