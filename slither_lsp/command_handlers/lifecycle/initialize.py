from typing import Any

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import WorkspaceFolder
from slither_lsp.types.lsp_params import InitializeParams, InitializeResult


class InitializeHandler(BaseCommandHandler):
    """
    Handler for the 'initialize' request, which exchanges capability/workspace information.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#initialize
    """
    method_name = "initialize"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        # Parse our initialization params
        params: InitializeParams = InitializeParams.from_dict(params)

        # Store some information in our server context
        context.client_info = params.client_info
        context.trace = params.trace

        # Obtain workspace information. If we couldn't obtain any, try the older deprecated uri param
        context.workspace_folders = params.workspace_folders or []
        if len(context.workspace_folders) == 0:
            if params.root_uri is not None:
                context.workspace_folders = [
                    WorkspaceFolder(name=None, uri=params.root_uri)
                ]

        # Parse client capabilities
        context.client_capabilities = params.capabilities

        # Set our server as initialized, trigger relevant event
        context.server_initialized = True
        context.event_emitter.emit('server.initialized')

        # Return our server capabilities
        return InitializeResult(context.server_capabilities, context.server_info).to_dict()
