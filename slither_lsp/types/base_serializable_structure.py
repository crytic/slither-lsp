from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Set


class SerializableStructure(ABC):
    """
    Represents a structure which is serializable to/deserializable from generic LSP structures.
    """
    def __init__(self, **kwargs):
        """
        Empty constructor, overriden by the @dataclass property. This simply satisfies the linter when instantiating
        with arbitary arguments.
        :param kwargs: Arbitrary argument array.
        """
        pass

    @classmethod
    def from_dict(cls, obj: dict) -> 'SerializableStructure':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        # Create our dictionary
        init_args: dict = {}
        cls._init_args_from_dict(init_args, obj)

        # Use the parsed arguments to instantiate a copy of this class
        return cls(**init_args)

    @classmethod
    @abstractmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def to_dict(self, result: Optional[dict] = None) -> dict:
        """
        Dumps an instance of this class to a dictionary object. It reads all relevant properties for this immediate
        class and classes it had inherited from.
        :param result: The dictionary to put serialized values into. If none, creates a new dictionary.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        raise NotImplementedError()
