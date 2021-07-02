from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.types.errors import CapabilitiesNotSupportedError
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import DidChangeWorkspaceFoldersParams


class DidChangeWorkspaceFolderHandler(BaseRequestHandler):
    """
    Handler for the 'workspace/didChangeWorkspaceFolders' notification, which notifies the server that the client
    added or removed workspace folders.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_didChangeWorkspaceFolders
    """

    method_name = "workspace/didChangeWorkspaceFolders"

    @classmethod
    def _check_capabilities(cls, context: ServerContext) -> None:
        """
        Checks if the client has capabilities for this message. Throws a CapabilitiesNotSupportedError if it does not.
        :param context: The server context which tracks state for the server.
        :return: None
        """

        server_supported: bool = context.server_capabilities.workspace and \
            context.server_capabilities.workspace.workspace_folders and \
            context.server_capabilities.workspace.workspace_folders.supported
        if not server_supported:
            raise CapabilitiesNotSupportedError(cls)

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'workspace/didChangeWorkspaceFolders' notification which indicates that workspace folders were added
        or removed.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_didChangeWorkspaceFolders
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: None
        """
        # Verify we have appropriate capabilities
        cls._check_capabilities(context)

        # Validate the structure of our request
        params: DidChangeWorkspaceFoldersParams = DidChangeWorkspaceFoldersParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'workspace.didChangeWorkspaceFolders',
            params=params
        )

        # This is a notification so we return nothing
        return None
