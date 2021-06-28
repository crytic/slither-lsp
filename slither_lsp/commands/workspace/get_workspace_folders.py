from typing import Any, Optional, List

from slither_lsp.commands.base_command import BaseCommand
from slither_lsp.state.server_context import ServerContext
from slither_lsp.errors.lsp_errors import CapabilitiesNotSupportedError
from slither_lsp.types.lsp_basic_structures import WorkspaceFolder


class GetWorkspaceFoldersRequest(BaseCommand):
    """
    Command which obtains an array of workspace folders.
    """

    method_name = "workspace/workspaceFolders"

    @classmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
        """
        Checks if the client has capabilities for this command.
        :param context: The server context which tracks state for the server.
        :return: A boolean indicating whether the client has appropriate capabilities to run this command.
        """
        return context.client_capabilities.workspace and context.client_capabilities.workspace.workspace_folders

    @classmethod
    def send(cls, context: ServerContext) -> List[WorkspaceFolder]:
        """
        Sends a 'workspace/workspaceFolders' request to the client to obtain workspace folders.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_showMessage
        :param context: The server context which determines the server to use to send the message.
        :return: None
        """
        # Throw an exception if we don't support the underlying capabilities.
        if not cls.has_capabilities(context):
            raise CapabilitiesNotSupportedError(cls)

        # Invoke the operation otherwise.
        workspace_folders = context.server.send_request_message(
            cls.method_name,
            None
        )

        # Verify our result is a list
        if not isinstance(workspace_folders, list):
            raise ValueError(f'{cls.method_name} request returned a non list type response.')

        # Parse our data
        workspace_folders = [WorkspaceFolder.from_dict(folder) for folder in workspace_folders]
        return workspace_folders
