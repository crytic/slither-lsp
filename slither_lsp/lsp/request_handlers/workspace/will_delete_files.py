from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.errors import CapabilitiesNotSupportedError
from slither_lsp.lsp.types.params import DeleteFilesParams


class WillDeleteFilesHandler(BaseRequestHandler):
    """
    Handler for the 'workspace/willDeleteFiles' notification, which is sent from the client to the server before files
    are actually deleted as long as the deletion is triggered from within the client either by a user action or by
    applying a workspace edit.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_willDeleteFiles
    """

    method_name = "workspace/willDeleteFiles"

    @classmethod
    def _check_capabilities(cls, context: ServerContext) -> None:
        """
        Checks if the client has capabilities for this message. Throws a CapabilitiesNotSupportedError if it does not.
        :param context: The server context which tracks state for the server.
        :return: None
        """

        server_supported: bool = context.server_capabilities.workspace and \
            context.server_capabilities.workspace.file_operations and \
            context.server_capabilities.workspace.file_operations.will_delete is not None
        if not server_supported:
            raise CapabilitiesNotSupportedError(cls)

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'workspace/willDeleteFiles' notification which is sent from the client to the server before files are
        actually deleted as long as the deletion is triggered from within the client either by a user action or by
        applying a workspace edit.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_willDeleteFiles
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: None
        """
        # Verify we have appropriate capabilities
        cls._check_capabilities(context)

        # Validate the structure of our request
        params: DeleteFilesParams = DeleteFilesParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'workspace.willDeleteFiles',
            params=params
        )

        # This is a notification so we return nothing
        return None
