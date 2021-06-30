from abc import ABC, abstractmethod
from typing import Any

from slither_lsp.lsp.state.server_context import ServerContext


class BaseRequestHandler(ABC):
    """
    Represents a handler for a request or notification provided over the Language Server Protocol.
    """

    @staticmethod
    @abstractmethod
    def method_name():
        """
        The name of the method which this request/notification handler handles. This should be unique per
        handler. Handlers which are custom or client/server-specific should be prefixed with '$/'
        :return: The name of the method which this request/notification handler handles.
        """
        pass

    @staticmethod
    @abstractmethod
    def process(context: ServerContext, params: Any) -> Any:
        pass
