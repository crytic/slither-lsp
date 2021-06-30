from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext


class ExitHandler(BaseRequestHandler):
    """
    Handler for the 'exit' notification, which signals that the language server should shut down.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#exit
    """
    method_name = "exit"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:

        # TODO: Find a more elegant way to exit and make sure all important operations were torn down.
        import sys
        sys.exit(0)
