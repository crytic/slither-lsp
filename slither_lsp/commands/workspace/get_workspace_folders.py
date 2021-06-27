from typing import Any, Optional

from slither_lsp.commands.base_command import BaseCommand
from slither_lsp.state.server_context import ServerContext
from slither_lsp.errors.lsp_errors import LSPCommandNotSupported


class GetWorkspaceFoldersRequest(BaseCommand):
    """
    Command which obtains an array of workspace folders.
    """

    method_name = "workspace/workspaceFolders"

    @classmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
        """
        Checks if the client and server have capabilities for this command.
        :param context: The server context which tracks state for the server.
        :return: A boolean indicating whether the client and server have appropriate capabilities to run this command.
        """
        client_supported: bool = context.client_capabilities.get_from_path(
            ['workspace', 'workspaceFolders'],
            default=False,
            enforce_type=bool
        )
        server_supported: bool = context.server_capabilities.get_from_path(
            ['workspace', 'workspaceFolders', 'supported'],
            default=False,
            enforce_type=bool
        )
        return client_supported and server_supported

    @classmethod
    def send(cls, context: ServerContext) -> Any:
        """
        Sends a 'workspace/workspaceFolders' request to the client to obtain workspace folders.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_showMessage
        :param context: The server context which determines the server to use to send the message.
        :return: None
        """
        # Throw an exception if we don't support the underlying capabilities.
        if not cls.has_capabilities(context):
            LSPCommandNotSupported.from_command(cls)

        # Invoke the operation otherwise.
        workspace_folders = context.server.send_request_message(
            cls.method_name, None
        )
        return workspace_folders
