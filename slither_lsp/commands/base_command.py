from abc import ABC, abstractmethod

from slither_lsp.errors.lsp_errors import LSPCommandNotSupported
from slither_lsp.state.server_context import ServerContext


def requires_capabilities(func):
    """
    Decorator intended for functions in a BaseCommand which calls has_capabilities prior to calling the function.
    :param func: The function within a BaseCommand to wrap with a decorator.
    :return:
    """
    def wrapper(cls=None, context: ServerContext = None, *args, **kwargs):
        # If the class is not a base command, raise an exception
        if not issubclass(cls, BaseCommand):
            raise ValueError(
                "Capabilities could not be checked on this function because the parent command class could not be "
                "identified."
            )

        # If we have capabilities, call the function (positional argument order is important), otherwise raise an
        # exception.
        if context is not None and cls.has_capabilities(context):
            return func(cls, context, *args)
        else:
            raise LSPCommandNotSupported(
                f"'{cls.method_name}' is not supported due to client/server capabilities."
            )

    return wrapper


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
        Checks if the client and server have capabilities for this command.
        :param context: The server context which tracks state for the server.
        :return: A boolean indicating whether the client and server have appropriate capabilities to run this command.
        """
        raise NotImplementedError()


class BaseCommandWithDynamicCapabilities(BaseCommand):
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