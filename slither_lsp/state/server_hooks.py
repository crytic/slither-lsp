from abc import ABC, abstractmethod
from typing import Union, List

from slither_lsp.state.server_context import ServerContext
from slither_lsp.types.lsp_basic_structures import Location, LocationLink
from slither_lsp.types.lsp_params import DeclarationParams, DefinitionParams, TypeDefinitionParams, ImplementationParams


class ServerHooks(ABC):
    """
    Defines a set of hooks which the server can use to implement command responses.
    """

    @abstractmethod
    def goto_declaration(self, context: ServerContext, params: DeclarationParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        """
        Resolves a declaration location of a symbol at a given text document position.
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: Location | Location[] | LocationLink[] | None
        """
        return None

    @abstractmethod
    def goto_definition(self, context: ServerContext, params: DefinitionParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        """
        Resolves a definition location of a symbol at a given text document position.
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: Location | Location[] | LocationLink[] | None
        """
        return None

    @abstractmethod
    def goto_type_definition(self, context: ServerContext, params: TypeDefinitionParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        """
        Resolves a type definition location of a symbol at a given text document position.
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: Location | Location[] | LocationLink[] | None
        """
        return None

    @abstractmethod
    def goto_implementation(self, context: ServerContext, params: ImplementationParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        """
        Resolves a implementation location of a symbol at a given text document position.
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: Location | Location[] | LocationLink[] | None
        """
        return None

    @abstractmethod
    def find_references(self, context: ServerContext, params: ImplementationParams) \
            -> Union[List[Location], None]:
        """
        Resolves project-wide references for the symbol denoted by the given text document position.
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this command.
        :return: Location[] | None
        """
        return None
