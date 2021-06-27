import inspect
import traceback
from threading import Lock, Thread
from time import sleep
from typing import Any, Callable, Dict, IO, Optional, Type, Tuple, Union

from pymitter import EventEmitter

from slither_lsp.command_handlers import registered_handlers
from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.command_handlers.lifecycle.exit import ExitHandler
from slither_lsp.errors.lsp_errors import LSPError, LSPErrorCode
from slither_lsp.io.jsonrpc_io import JsonRpcIo
from slither_lsp.state.capabilities import Capabilities
from slither_lsp.state.server_context import ServerContext

# Register all imported command handlers so we have a lookup of method name -> handler
COMMAND_HANDLERS = [getattr(registered_handlers, name) for name in dir(registered_handlers)]
COMMAND_HANDLERS = {
    ch.method_name: ch
    for ch in COMMAND_HANDLERS
    if inspect.isclass(ch) and ch != BaseCommandHandler and issubclass(ch, BaseCommandHandler)
}

HANDLER_POLLING_INTERVAL: float = 0.1
RESPONSE_POLLING_INTERVAL: float = 0.1


class BaseServer:
    """
    TODO:
    """
    def __init__(self, server_capabilities: Capabilities):
        self.running: bool = False
        self.context: Optional[ServerContext] = None
        self.io: Optional[JsonRpcIo] = None
        self._pending_response_queue: Dict[Union[int, str], Optional[Any]] = {}
        self._current_server_request_id = 0
        self._request_lock = Lock()
        self._init_server_capabilities: Capabilities = server_capabilities

        # Create our main event emitter
        self.event_emitter = EventEmitter()

    def _main_loop(self, read_file_handle: IO, write_file_handle: IO):
        """
        The main entry point for the server, which begins accepting and processing command_handlers
        on the given IO.
        :return: None
        """
        # Set our running state to True
        self.running = True

        # Reset server state and set our IO
        server_capabilities = self._init_server_capabilities.clone() if self._init_server_capabilities is not None else None
        self.context = ServerContext(self, server_capabilities=server_capabilities)
        self.io = JsonRpcIo(read_file_handle, write_file_handle)

        # Continuously process messages.
        # TODO: This should use proper controls and not loop endlessly, potentially draining
        #  resources.
        while True:
            try:
                # Read a message, if there is none available, loop and wait for another.
                result = self.io.read()
                if result is None:
                    sleep(HANDLER_POLLING_INTERVAL)
                    continue

                # Process the underlying message
                (headers, message) = result
                self._handle_message(message)
            except ConnectionResetError as e:
                # If the connection was reset, we exit the LSP using the exit handler
                # (so a clean exit is invoked).
                ExitHandler.process(self.context, None)

    def _handle_message(self, message: Any) -> None:
        """
        The main dispatcher for a received message. It handles a request, notification, or response for a previously
        made request.
        :param message: The deserialized Language Server Protocol message received over JSON-RPC.
        :return: None
        """

        # Verify the top level is a dictionary
        if not isinstance(message, dict):
            # This should be a dictionary at the top level, but we'll ignore requests that are
            # malformed this bad.
            return

        # If there's a method field, its a request or notification. If there isn't, it's a response
        method_name = message.get('method')
        if method_name is not None:
            self._handle_request_or_notification(message)
        else:
            self._handle_response(message)

    def _handle_request_or_notification(self, message: Any) -> None:
        """
        The dispatcher for a received request or notification. It determines which command handler to call and unpacks
        arguments.
        :param message: The deserialized Language Server Protocol message received over JSON-RPC.
        :return: None
        """
        # Fetch basic parameters
        message_id = message.get('id')
        method_name = message.get('method')

        # This should be a request or notification.
        try:
            # If the method name isn't a string, throw an invalid request error.
            if not isinstance(method_name, str):
                raise LSPError(
                    LSPErrorCode.InvalidRequest,
                    "'method' field should be a string type.",
                    None
                )

            # If this is a request and we're shutdown, return an error.
            if message_id is None and self.context.shutdown:
                raise LSPError(
                    LSPErrorCode.InvalidRequest,
                    "Cannot process additional requests once a shutdown request has been made.",
                    None
                )

            # Fetch the relevant command handler. If we don't have one, raise an error.
            command_handler: Optional[Type[BaseCommandHandler]] = COMMAND_HANDLERS.get(method_name)
            if command_handler is None:
                raise LSPError(
                    LSPErrorCode.MethodNotFound,
                    f"A command handler does not exist for method '{method_name}'",
                    None,
                )

            # Execute the relevant command handler and get the result.
            try:
                result = command_handler.process(self.context, message.get('params'))
            except LSPError as err:
                # If it's an LSPError, we simply re-raise it without wrapping it.
                raise err
            except Exception as err:
                # Wrap any other exception in an LSPError exception and raise it
                traceback_str = traceback.format_exc()
                raise LSPError(
                    LSPErrorCode.InternalError,
                    f"An unhandled exception occurred:\r\n{traceback_str}",
                    traceback_str
                ) from err

            # If we have a message id, it is a request, so we send back a response.
            # Otherwise it's a notification and we don't do anything.
            if message_id is not None:
                self._send_response_message(message_id, result)

        except LSPError as lsp_error:
            # If an LSP error occurred, we send it over the wire.
            self._send_response_error(
                message_id,
                lsp_error.error_code,
                lsp_error.error_message,
                lsp_error.error_data
            )

    def _handle_response(self, message: Any) -> None:
        """
        Handles a response from the client for a previously sent request.
        :param message: The deserialized Language Server Protocol message received over JSON-RPC.
        :return: None
        """
        # Fetch basic parameters
        message_id = message.get('id')

        # Ignore responses without an id or callback functions.
        if message_id is None or (not isinstance(message_id, str) and not isinstance(message_id, int)):
            return

        # Determine if this is an error or success result.
        error_info = message.get('error')
        if error_info is not None:
            # We had an error result, unpack our error fields.
            # TODO: If the error is malformed, we should introduce window here later.
            #  For now we ignore.
            if not isinstance(error_info, dict):
                return

            error_code: Optional[int] = error_info.get('code')
            error_message: Optional[str] = error_info.get('message')
            error_data: Any = error_info.get('data')

            # TODO: If the error is malformed, we should introduce window here later.
            #  For now we ignore.
            self._pending_response_queue[message_id] = LSPError(LSPErrorCode(error_code), error_message, error_data)
        else:
            # We had a successful result.
            self._pending_response_queue[message_id] = message.get('result')

    def send_request_message(self, method_name: str, params: Any) -> Any:
        """
        Sends a request to the client, providing callback options in the event of success/error.
        :param method_name: The name of the method to invoke on the client.
        :param params: The parameters to send with the request.
        :return: None
        """
        # Lock to avoid request id collisions
        with self._request_lock:
            # Generate a request id
            request_id: Union[str, int] = f"slither-lsp-{self._current_server_request_id}"

            # Increment the request id
            self._current_server_request_id += 1

        # Send the request to the client
        self.io.write({
            'jsonrpc': '2.0',
            'id': request_id,
            'method': method_name,
            'params': params
        })

        # Wait for a response
        while request_id not in self._pending_response_queue:
            sleep(RESPONSE_POLLING_INTERVAL)

        # Obtain the response from the queue. If it was an LSP error, raise it.
        response = self._pending_response_queue.pop(request_id)
        if isinstance(response, LSPError):
            raise LSPError(
                LSPErrorCode.InternalError,
                f"Request '{method_name}' failed:\r\n{response.error_message}",
                None
            )

        # Return the response data
        return response

    def _send_response_message(self, message_id: Union[int, str, None], result: Any) -> None:
        """
        Sends a response back to the client in the event of a successful operation.
        :param message_id: The message id to respond to with this message.
        :param result: The resulting data to respond with in response to a previous request which used message_id.
        :return: None
        """
        self.io.write({
            'jsonrpc': '2.0',
            'id': message_id,
            'result': result
        })

    def _send_response_error(self, message_id: Union[int, str, None], error_code: LSPErrorCode, error_message: str,
                             error_data: Any) -> None:
        """
        Sends an error response back to the client.
        :param message_id: The message id to respond to with this error.
        :param error_code: The error code to send across the wire.
        :param error_message: A short description of the error to be supplied to the client.
        :param error_data: Optional additional data which can be included with the error.
        :return: None
        """
        self.io.write({
            'jsonrpc': '2.0',
            'id': message_id,
            'error': {
                'code': int(error_code),
                'message': error_message,
                'data': error_data
            }
        })

    def send_notification_message(self, method_name: str, params: Any) -> None:
        """
        Sends a notification to the client which targeting a specific method.
        :param method_name: The name of the method to invoke with this notification.
        :param params: The additional data provided to the underlying method.
        :return: None
        """
        self.io.write({
            'jsonrpc': '2.0',
            'method': method_name,
            'params': params
        })
