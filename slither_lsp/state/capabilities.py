from typing import Any, List, Optional


class Capabilities:
    """
    Capabilities wrapper for the internal capabilities object.
    """
    def __init__(self, data: dict = None):
        """
        The constructor for the capabilities object.
        :param data: The underlying client/server capabilities object.
        """
        # Initialize our capabilities with this data
        if data is None:
            self._data = {}
        else:
            self._data = data

    def get_from_path(self, path: List[str], default: Any = None, enforce_type: Optional[type] = None
    ) -> Any:
        """
        Obtains a value from the internal capability data at the given path. If it does not exist, the default value
        provided is returned.
        :param path: The key path to obtain a value from in the internal capability data.
        :param default: The default value to return if no value at the key path exists.
        :param enforce_type: An optional type to enforce on the return value, otherwise the default value is returned.
        :return: Returns the value at the given key path in the internal capability data, otherwise returns the
        default value.
        """
        # Iterate over our path until we arrive at our destination.
        result = self._data

        for key in path:
            # If the key in this part of the path doesn't exist, neither does our value
            if key not in result:
                return default

            # Verify this is a dictionary before we try to obtain the value at this path
            if not isinstance(result, dict):
                return default

            # Obtain the value for this key.
            result = result.get(key)

        # If we're enforcing type and this is the wrong type, return a default value instead.
        if enforce_type is not None and not isinstance(result, enforce_type):
            return default

        # Return our result
        return result

    def set_at_path(self, path: List[str], value: Any) -> None:
        """
        Sets a value in the internal capability data at the given path. If the path does not exist, dictionaries are
        created for every key before the value is finally placed at the correct location.
        :param path: The key path to set a value at in the internal capability data.
        :param value: Sets the value at the given key path in the internal capability data.
        :return: None
        """
        # Iterate over our path until we arrive at our destination.
        result = self._data

        for i, key in enumerate(path):
            # If the key in this part of the path doesn't exist, create a dictionary here
            if key not in result:
                result[key] = {}

            # Verify this is a dictionary before we try to obtain the value at this path
            if not isinstance(result, dict):
                raise ValueError(
                    "Could not set value at key path because a key-value pair was not a dictionary as expected."
                )

            # If this isn't the last item, iterate, otherwise, set our value
            if i < len(path) - 1:
                result = result.get(key)
            else:
                result[key] = value
                return

    @property
    def data(self) -> dict:
        """
        The internal capability data which this object represents.
        :return: Returns the internal capability data.
        """
        return self._data


class ServerCapabilities(Capabilities):
    """
    Server Capabilities wrapper which manages underlying capability properties.
    """
    def __init__(self):
        super().__init__(
            {
                # TODO: Relay server capabilities to the client.
                "workspace": {
                    "workspaceFolders": {
                        # The server supports workspace folders
                        "supported": True,

                        # changeNotifications is a boolean which indicates we want workspace change notifications,
                        # or it is a string which is meant to be an ID which the notification is registered on the
                        # client side. It can later be unregistered using a unregister capability request.
                        # "changeNotifications": True
                    }
                }
            }
        )


class ClientCapabilities(Capabilities):
    """
    Client Capabilities wrapper which manages underlying capability properties.
    """
