from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from slither_lsp.state.server_context import ServerContext


class BaseCommand(ABC):
    """
    Represents a command provider for the Language Server Protocol.
    Requests or Notifications should be implemented on top of this.
    """

    @staticmethod
    @abstractmethod
    def method_name(cls):
        """
        The name of the method which this command handler handles. This should be unique per
        handler. Handlers which are custom or client/server-specific should be prefixed with '$/'
        :return: The name of the method which this command handler handles.
        """
        pass

    @classmethod
    @abstractmethod
    def has_capabilities(cls, context: ServerContext) -> bool:
        """
        Checks if the client and server have the capabilities to support this command.
        :param context: The server context which determines the server/state to use to send the message.
        :return: A boolean indicating if the client and server are capable of carrying this command out.
        """
        raise NotImplementedError()


class BaseCommandWithDynamicCapabilities:
    """
    Represents a command provider for the Language Server protocol which supports dynamic capability registrations.
    Requests or Notifications which support dynamic capabilities should be implemented on top of this.
    """
    @classmethod
    @abstractmethod
    def register_capability(cls, context: ServerContext) -> None:
        """
        Registers a relevant server capability with the client.
        :param context: The server context which determines the server/state to use to send the message.
        :return: Returns any value necessary depending on the implementing command.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def unregister_capability(cls, context: ServerContext) -> None:
        """
        Unregisters a relevant server capability with the client.
        :param context: The server context which determines the server/state to use to send the message.
        :return: Returns any value necessary depending on the implementing command.
        """
        raise NotImplementedError()