from enum import IntEnum
from typing import Any, Union, Type

# pylint: disable=invalid-name
from slither_lsp.commands.base_command import BaseCommand


class LSPErrorCode(IntEnum):
    """
    Defines a set of error codes for use with the Language Server Protocol.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#responseMessage
    """
    # Defined by JSON RPC
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603

    # This is the start range of JSON RPC reserved error codes.
    # It doesn't denote a real error code. No LSP error codes should
    # be defined between the start and end range. For backwards
    # compatibility the `ServerNotInitialized` and the `UnknownErrorCode`
    # are left in the range.
    # @since 3.16.0
    jsonrpcReservedErrorRangeStart = -32099
    # @deprecated use jsonrpcReservedErrorRangeStart
    serverErrorStart = jsonrpcReservedErrorRangeStart

    # Error code indicating that a server received a notification or
    # request before the server has received the `initialize` request.
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001

    # This is the start range of JSON RPC reserved error codes.
    # It doesn't denote a real error code.
    # @since 3.16.0
    jsonrpcReservedErrorRangeEnd = -32000
    # @deprecated use jsonrpcReservedErrorRangeEnd
    serverErrorEnd = jsonrpcReservedErrorRangeEnd

    # This is the start range of LSP reserved error codes.
    # It doesn't denote a real error code.
    # @since 3.16.0
    lspReservedErrorRangeStart = -32899

    ContentModified = -32801
    RequestCancelled = -32800

    # This is the end range of LSP reserved error codes.
    # It doesn't denote a real error code.
    # @since 3.16.0
    lspReservedErrorRangeEnd = -32800


class LSPError(Exception):
    """
    Represents an LSP error, which when thrown in a command handler will be sent to the LSP client.
    """
    def __init__(self, code: LSPErrorCode, message: str, data: Any = None):
        self.error_code = code
        self.error_message = message
        self.error_data = data
        super().__init__()


class LSPCommandNotSupported(LSPError):
    """
    Represents an exception which is thrown when a command (request/notification) is invoked but is not supported
    by the client or server.
    """
    def __init__(self, message: str, code: LSPErrorCode = LSPErrorCode.InternalError, data: Any = None):
        super().__init__(code, message, data)

    @staticmethod
    def from_command(command: Union[BaseCommand, Type[BaseCommand]]) -> 'LSPCommandNotSupported':
        """
        Generates a generic exception for a given command.
        :param command: The command to create an exception for.
        :return: Returns an instance of this exception.
        """
        return LSPCommandNotSupported(f"'{command.method_name}' is not supported due to client/server capabilities.")
