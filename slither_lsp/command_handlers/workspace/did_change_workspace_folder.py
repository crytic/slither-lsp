from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.errors.lsp_errors import CapabilitiesNotSupportedError
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_params import DidChangeWorkspaceFoldersParams


class DidChangeWorkspaceFolderHandler(BaseCommandHandler):
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
        Checks if the client has capabilities for this command. Throws a CapabilitiesNotSupportedError if it does not.
        :param context: The server context which tracks state for the server.
        :return: None
        """

        client_supported: bool = context.client_capabilities.workspace and \
            context.client_capabilities.workspace.workspace_folders
        server_supported: bool = context.server_capabilities.workspace and \
            context.server_capabilities.workspace.workspace_folders and \
            context.server_capabilities.workspace.workspace_folders.supported
        if not client_supported and server_supported:
            raise CapabilitiesNotSupportedError(cls)

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'workspace/didChangeWorkspaceFolders' notification which indicates that workspace folders were added
        or removed.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_didChangeWorkspaceFolders
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: None
        """
        # Verify we have appropriate capabilities
        cls._check_capabilities(context)

        # Validate the structure of our request
        params: DidChangeWorkspaceFoldersParams = DidChangeWorkspaceFoldersParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'workspace.didChangeWorkspaceFolders',
            added=params.event.added,
            removed=params.event.removed
        )

        # This is a notification so we return nothing
        return None
