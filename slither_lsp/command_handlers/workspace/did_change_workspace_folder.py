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
    def has_capabilities(cls, context: ServerContext) -> bool:
        """
        Checks if the client and server have capabilities for this command.
        :param context: The server context which tracks state for the server.
        :return: A boolean indicating whether the client and server have appropriate capabilities to run this command.
        """

        client_supported: bool = context.client_capabilities.workspace and \
                                 context.client_capabilities.workspace.workspace_folders
        server_supported: bool = context.server_capabilities.workspace and \
                                 context.server_capabilities.workspace.workspace_folders and \
                                 context.server_capabilities.workspace.workspace_folders.supported
        return client_supported and server_supported

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Sends a 'workspace/workspaceFolders' request to the client to obtain workspace folders.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_showMessage
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: None
        """
        # Throw an exception if we don't support the underlying capabilities.
        if not cls.has_capabilities(context):
            raise CapabilitiesNotSupportedError(cls)

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
