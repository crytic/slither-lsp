from typing import Any

from slither.__main__ import get_detectors_and_printers, output_detectors_json

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.state.server_context import ServerContext


class GoToDeclarationHandler(BaseCommandHandler):
    """
    Handler for the 'textDocument/declaration' request, which resolves a declaration location of a symbol at a
    given text document position.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_declaration
    """
    method_name = "textDocument/declaration"

    @classmethod
    def _check_capabilities(cls, context: ServerContext) -> None:
        """
        Checks if the client has capabilities for this command. Throws a CapabilitiesNotSupportedError if it does not.
        :param context: The server context which tracks state for the server.
        :return: None
        """

        # TODO: Define and check capabilities.
        pass

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'textDocument/declaration' request and attempts to resolve a declaration location of a symbol at a
        given text document position.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_declaration
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: None
        """
        # Verify we have appropriate capabilities
        cls._check_capabilities(context)

        # TODO: Parse our request


        # Emit relevant events
        context.event_emitter.emit(
            'workspace.didChangeWorkspaceFolders',
            added=params.event.added,
            removed=params.event.removed
        )