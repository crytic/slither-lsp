from typing import Any, Optional

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.capabilities import Capabilities
from slither_lsp.state.server_context import ServerContext
from slither_lsp.errors.lsp_errors import CapabilitiesNotSupportedError, LSPError, LSPErrorCode
from slither_lsp.types.lsp_basic_structures import WorkspaceFolder


class DidChangeWorkspaceFolderHandler(BaseCommandHandler):
    """
    Handler for the 'workspace/didChangeWorkspaceFolders' notification, which notifies the server that the client
    added or removed workspace folders.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_didChangeWorkspaceFolders
    """

    method_name = "workspace/didChangeWorkspaceFolders"

    @classmethod
    def enable_server_capabilities(cls, capabilities: Capabilities, change_notifications: bool) -> None:
        """
        Enables capabilities on a server Capabilities object to signal our interest in workspace folder changes.
        :param capabilities: The server capabilities to modify.
        :param change_notifications: A boolean indicating whether we want the client to notify us of changes to
        workspace folders.
        :return: None
        """
        capabilities.set('workspace.workspaceFolders.supported', True)
        if change_notifications:
            capabilities.set('workspace.workspaceFolders.changeNotifications', True)

    @classmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
        """
        Checks if the client and server have capabilities for this command.
        :param context: The server context which tracks state for the server.
        :return: A boolean indicating whether the client and server have appropriate capabilities to run this command.
        """
        client_supported: bool = context.client_capabilities.get(
            'workspace.workspaceFolders',
            default=False,
            enforce_type=bool
        )
        server_supported: bool = context.server_capabilities.get(
            'workspace.workspaceFolders.supported',
            default=False,
            enforce_type=bool
        )
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
        event: Optional[dict] = params.get('event')
        if event is None:
            raise LSPError(
                LSPErrorCode.InvalidParams,
                "'event' key was not provided.",
                None
            )

        # Our event should have an added and removed array
        added = event.get('added') or []
        removed = event.get('removed') or []
        if not (isinstance(added, list) or isinstance(removed, list)):
            raise LSPError(
                LSPErrorCode.InvalidParams,
                "'added' and 'removed' values must be lists.",
                None
            )

        # Parse each array
        added = [WorkspaceFolder.from_dict(workspace_folder_info) for workspace_folder_info in added]
        removed = [WorkspaceFolder.from_dict(workspace_folder_info) for workspace_folder_info in removed]

        # Emit relevant events
        context.event_emitter.emit('workspace.didChangeWorkspaceFolders', added=added, removed=removed)

        # This is a notification so we return nothing
        return None
