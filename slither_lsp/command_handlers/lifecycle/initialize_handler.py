from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from typing import Any
from slither_lsp.state.server_context import ServerContext
from slither_lsp.errors.lsp_error import LSPErrorCode, LSPError
from slither_lsp.types.server_enums import TraceValue
from pkg_resources import require


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
        context.client_name = None
        context.client_version = None
        client_info = params.get('clientInfo')
        if client_info is not None and isinstance(client_info, dict):
            context.client_name = client_info.get('name')
            context.client_version = client_info.get('version')

        # Parse trace level
        trace_level = params.get('trace')
        if trace_level is not None and isinstance(trace_level, str):
            context.trace = trace_level

        # Obtain the workspace folders
        context.workspace_uris = []
        workspace_folders = params.get('workspaceFolders')
        if workspace_folders is not None and isinstance(workspace_folders, list):
            for workspace_folder in workspace_folders:
                if isinstance(workspace_folder, dict):
                    workspace_uri = workspace_folder.get('uri')
                    if workspace_uri is not None and isinstance(workspace_uri, str):
                        context.workspace_uris.append(workspace_uri)

        # If we couldn't obtain any, try the older deprecated uri param
        if len(context.workspace_uris) == 0:
            workspace_uri = params.get('rootUri')
            if workspace_uri is not None and isinstance(workspace_uri, str):
                context.workspace_uris.append(workspace_uri)

        # TODO: Parse client capabilities

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

