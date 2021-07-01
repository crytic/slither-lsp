from typing import List

from slither_lsp.lsp.requests.base_request import BaseRequest
from slither_lsp.lsp.types.errors import CapabilitiesNotSupportedError
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.basic_structures import WorkspaceFolder


class GetWorkspaceFoldersRequest(BaseRequest):
    """
    Request which obtains an array of workspace folders.
    """

    method_name = "workspace/workspaceFolders"

    @classmethod
    def _check_capabilities(cls, context: ServerContext) -> None:
        """
        Checks if the client has capabilities for this message. Throws a CapabilitiesNotSupportedError if it does not.
        :param context: The server context which tracks state for the server.
        :return: None
        """
        if not (context.client_capabilities.workspace and context.client_capabilities.workspace.workspace_folders):
            raise CapabilitiesNotSupportedError(cls)

    @classmethod
    def send(cls, context: ServerContext) -> List[WorkspaceFolder]:
        """
        Sends a 'workspace/workspaceFolders' request to the client to obtain workspace folders.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#window_showMessage
        :param context: The server context which determines the server to use to send the message.
        :return: None
        """
        # Check relevant capabilities
        cls._check_capabilities(context)

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
