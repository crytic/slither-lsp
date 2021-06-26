from typing import Any

from slither_lsp.commands.base_command import BaseCommandWithDynamicCapabilities
from slither_lsp.state.server_context import ServerContext
from slither_lsp.errors.lsp_errors import LSPCommandNotSupported


class GetWorkspaceFoldersRequest(BaseCommandWithDynamicCapabilities):
    """
    Command which obtains an array of workspace folders.
    """
    method_name = "workspace/workspaceFolders"

    @classmethod
    def register_capability(cls, context: ServerContext) -> None:
        # TODO: There is a dynamic capability for this, add support for it.
        raise NotImplementedError()

    @classmethod
    def unregister_capability(cls, context: ServerContext) -> None:
        # TODO: There is a dynamic capability for this, add support for it.
        raise NotImplementedError()

    @classmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
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
        # Raise an exception if this command is unsupported
        if not cls.has_capabilities(context):
            raise LSPCommandNotSupported(
                f"'{cls.method_name}' is not supported due to client/server capabilities."
            )

        # Invoke the operation otherwise.
        workspace_folders = context.server.send_request_message(
            cls.method_name, None
        )
        return workspace_folders
