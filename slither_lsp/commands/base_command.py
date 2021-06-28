from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Represents a command provider for the Language Server Protocol.
    Requests or Notifications should be implemented on top of this.
    """

    @staticmethod
    @abstractmethod
    def method_name():
        """
        The name of the method which this command handler handles. This should be unique per
        handler. Handlers which are custom or client/server-specific should be prefixed with '$/'
        :return: The name of the method which this command handler handles.
        """
        pass
