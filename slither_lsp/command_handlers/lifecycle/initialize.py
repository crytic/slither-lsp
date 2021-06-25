from typing import Any

from pkg_resources import require

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.errors.lsp_error import LSPErrorCode, LSPError
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.workspace_types import ClientInfo, WorkspaceFolder


class InitializeHandler(BaseCommandHandler):
    """
    Handler for the 'initialize' request, which exchanges capability/workspace information.
    Reference: https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#initialize
    """
    method_name = "initialize"

    @staticmethod
    def process(context: ServerContext, params: Any) -> Any:
        # Verify params is the correct type
        if not isinstance(params, dict):
            raise LSPError(
                LSPErrorCode.InvalidParams,
                "Invalid params supplied. Expected a dictionary/structure type at the top level.",
                {'retry': True}
            )

        # Parse client info if it exists.
        context.client_info = None
        client_info = params.get('clientInfo')
        if client_info is not None and isinstance(client_info, dict):
            context.client_info = ClientInfo(name=client_info.get('name'), version=client_info.get('version'))

        # Parse trace level
        trace_level = params.get('trace')
        if trace_level is not None and isinstance(trace_level, str):
            context.trace = trace_level

        # Obtain the workspace folders
        context.workspace_folders = []
        workspace_folders = params.get('workspaceFolders')
        if workspace_folders is not None and isinstance(workspace_folders, list):
            context.workspace_folders = [
                WorkspaceFolder(name=workspace_folder.get('name'), uri=workspace_folder.get('uri'))
                for workspace_folder in workspace_folders
                if workspace_folder.get('uri')
            ]

        # If we couldn't obtain any, try the older deprecated uri param
        if len(context.workspace_folders) == 0:
            workspace_uri = params.get('rootUri')
            if workspace_uri is not None and isinstance(workspace_uri, str):
                context.workspace_folders = [
                    WorkspaceFolder(name=None, uri=workspace_uri)
                ]

        # Parse client capabilities
        context.client_capabilities = params.get('capabilities')

        # Set our server as initialized
        # TODO: Create and trigger an event for this.
        context.server_initialized = True

        return {
            'capabilities': {
                # TODO: Relay server capabilities to the client.
            },
            'serverInfo': {
                'name': 'Slither Language Server',
                'version': require("slither-analyzer")[0].version
            }
        }
