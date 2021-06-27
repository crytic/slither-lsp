from typing import Any

from pkg_resources import require

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.errors.lsp_errors import LSPErrorCode, LSPError
from slither_lsp.state.capabilities import Capabilities
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import ClientServerInfo, WorkspaceFolder, TraceValue


class InitializeHandler(BaseCommandHandler):
    """
    Handler for the 'initialize' request, which exchanges capability/workspace information.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#initialize
    """
    method_name = "initialize"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
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
            context.client_info = ClientServerInfo.from_dict(client_info)

        # Parse trace level
        trace_level = params.get('trace')
        if trace_level is not None and isinstance(trace_level, str):
            context.trace = TraceValue(trace_level)

        # Obtain the workspace folders
        context.workspace_folders = []
        workspace_folders = params.get('workspaceFolders')
        if workspace_folders is not None and isinstance(workspace_folders, list):
            context.workspace_folders = [
                WorkspaceFolder.from_dict(workspace_folder)
                for workspace_folder in workspace_folders
            ]

        # If we couldn't obtain any, try the older deprecated uri param
        if len(context.workspace_folders) == 0:
            workspace_uri = params.get('rootUri')
            if workspace_uri is not None and isinstance(workspace_uri, str):
                context.workspace_folders = [
                    WorkspaceFolder(name=None, uri=workspace_uri)
                ]

        # Parse client capabilities
        context.client_capabilities = Capabilities(params.get('capabilities'))

        # Set our server as initialized, trigger relevant event
        context.server_initialized = True
        context.event_emitter.emit('server.initialized')

        # Return our server capabilities
        return {
            'capabilities': context.server_capabilities.data,
            'serverInfo': context.server_info.to_dict()
        }
