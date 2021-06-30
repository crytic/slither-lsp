from typing import Union, List, Optional

from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.state.server_hooks import ServerHooks
from slither_lsp.lsp.types.basic_structures import Location, LocationLink
from slither_lsp.lsp.types.params import ImplementationParams, TypeDefinitionParams, DefinitionParams, DeclarationParams


class SlitherLSPHooks(ServerHooks):
    def __init__(self, app):
        # Late import to avoid circular reference issues
        from slither_lsp.app.app import SlitherLSPApp

        # Set our parameters.
        self.app: SlitherLSPApp = app

    def goto_declaration(self, context: ServerContext, params: DeclarationParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        return None

    def goto_definition(self, context: ServerContext, params: DefinitionParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        return None

    def goto_type_definition(self, context: ServerContext, params: TypeDefinitionParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        return None

    def goto_implementation(self, context: ServerContext, params: ImplementationParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        return None

    def find_references(self, context: ServerContext, params: ImplementationParams) \
            -> Optional[List[Location]]:
        return None
