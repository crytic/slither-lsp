from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.basic_structures import WorkspaceFolder
from slither_lsp.lsp.types.params import InitializeParams, InitializeResult


class InitializeHandler(BaseRequestHandler):
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

        # Create our initialization result
        result = InitializeResult(context.server_capabilities, context.server_info)

        # Set our server as initialized, trigger relevant event
        context.server_initialized = True
        context.event_emitter.emit(
            'server.initialized',
            params=params,
            result=result
        )

        # Return our server capabilities
        return result.to_dict()
