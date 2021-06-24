from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from typing import Any
from slither_lsp.state.server_context import ServerContext


class ExitHandler(BaseCommandHandler):
    """
    Handler for the 'exit' notification, which signals that the language server should shut down.
    Reference: https://microsoft.github.io/language-server-protocol/specifications/specification-3-16/#exit
    """
    method_name = "exit"

    @staticmethod
    def process(context: ServerContext, params: Any) -> Any:

        # TODO: Find a more elegant way to exit and make sure all important operations were torn down.
        import sys
        sys.exit(0)

