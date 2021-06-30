from abc import ABC, abstractmethod


class BaseRequest(ABC):
    """
    Represents a request/notification provider for the Language Server Protocol.
    Requests or Notifications should be implemented on top of this.
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
