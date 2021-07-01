import re
import inspect
from abc import ABC, abstractmethod
from dataclasses import fields, dataclass, is_dataclass
from enum import Enum, IntEnum
from typing import Any, Optional, Type, Set, List, Union, get_args, get_origin, Tuple


def _to_camel_case(s):
    """
    Converts a snake case string into a camel case string.
    :param s: The snake string to convert into camel case.
    :return: Returns the resulting camel case string.
    """
    # Split string on underscore. Output first part but capitalize the first letter of the other parts and join them.
    parts = s.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])


def _get_potential_types(obj_type: Type) -> Tuple[Optional[Type], List[Type]]:
    origin_type = get_origin(obj_type)
    args = get_args(obj_type)
    return origin_type, args


@dataclass
class _EmptyDataClass:
    """
    This class serves as a class with an unconfigured variable which is used to resolve the _MISSING type
    used to signal 'default' and 'default_factory' being unset.
    """
    plain_value: Any


# Obtain the type used for empty 'default' and 'default_factory' parameters.
_EMPTY_DEFAULT_TYPE = type(fields(_EmptyDataClass)[0].default)


def _get_default_value(field):
    """
    Obtains a default value for a given field.
    :param field: The field to obtain the default value for.
    :return: Returns a default value for a given field.
    """
    if not isinstance(field.default, _EMPTY_DEFAULT_TYPE):
        return field.default
    elif not isinstance(field.default_factory, _EMPTY_DEFAULT_TYPE):
        return field.default_factory()
    return None


def serialization_metadata(name_override: str = None, include_none: Optional[bool] = None,
                           enforce_as_constant: Optional[bool] = None) -> dict:
    """
    Creates metadata for python dataclasses, to be used with SerializableStructure to convey additional serialization
    information.
    :param name_override: If not None, denotes an override for the key name when serializing a dataclass field.
    :param include_none: If not None, denotes whether None/null keys should be included.
    :param enforce_as_constant: If not None, treats the default value as a constant which needs to be enforced strictly.
    :return: Returns a dictionary containing the metadata keys to be expected
    """
    metadata = {}
    if name_override is not None:
        metadata['name'] = name_override
    if include_none is not None:
        metadata['include_none'] = include_none
    if enforce_as_constant is not None:
        metadata['enforce_as_constant'] = enforce_as_constant
    return metadata


@dataclass
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

    def clone(self) -> 'SerializableStructure':
        """
        Creates a clone of the serializable object.
        :return: Returns a clone of this structured object.
        """
        return self.from_dict(self.to_dict())

    @classmethod
    def _serialize_field(cls, field_value: Any, field_type: Type) -> Any:
        # Obtain type information.
        origin_type, origin_type_args = _get_potential_types(field_type)

        # Obtain a list of types that satisfy this field. If this is a union, it's arguments are our satisfying types.
        satisfying_types: List[Type] = []
        if origin_type is Union:
            satisfying_types.extend(origin_type_args)
        else:
            satisfying_types.append(field_type)

        # If the value is None and we allow None types, return it. Otherwise throw an error.
        if field_value is None:
            if type(None) in satisfying_types or Any in satisfying_types:
                return None
            else:
                raise ValueError("Error deserializing field. Expected a non-None type, but got None")

        # It can't be a none type now, so remove it from our list of potential types
        if type(None) in satisfying_types:
            satisfying_types.remove(type(None))

        # Loop through all our satisfying types.
        for satisfying_type in satisfying_types:

            if inspect.isclass(satisfying_type):
                # Handle ints
                if satisfying_type is int and isinstance(field_value, int) or \
                        satisfying_type is str and isinstance(field_value, str) or \
                        satisfying_type is float and isinstance(field_value, float) or \
                        satisfying_type is bool and isinstance(field_value, bool):
                    return field_value

                # Handle enums
                if (issubclass(satisfying_type, IntEnum) and isinstance(field_value, satisfying_type)) or \
                        (satisfying_type is Any and isinstance(field_value, IntEnum)):
                    field_value: IntEnum
                    return field_value.value
                if (issubclass(satisfying_type, Enum) and isinstance(field_value, satisfying_type)) or \
                        (satisfying_type is Any and isinstance(field_value, Enum)):
                    field_value: Enum
                    return field_value.value

                # If our current satisfying type is a serializable structure and we have a dict, simply serialize it
                if (issubclass(satisfying_type, SerializableStructure) and isinstance(field_value, satisfying_type)) \
                        or (satisfying_type is Any and isinstance(field_value, SerializableStructure)):
                    return field_value.to_dict()

            # Handle lists if our field value is a list
            if isinstance(field_value, list):
                try:
                    # Obtain information about the satisfying type
                    if inspect.isclass(satisfying_type) and satisfying_type is list:
                        potential_list_origin_type = list
                        potential_list_element_types = []
                    else:
                        potential_list_origin_type, potential_list_element_types = _get_potential_types(satisfying_type)

                    if potential_list_origin_type is not None and issubclass(potential_list_origin_type, list):
                        # Obtain our element type. If we don't have one, we use 'Any' by default
                        element_type = Any
                        if len(potential_list_element_types) > 0:
                            element_type = potential_list_element_types[0]

                        # Deserialize the list accordingly.
                        serialized_list = [
                            cls._serialize_field(element, element_type)
                            for element in field_value
                        ]
                        return serialized_list
                except ValueError:
                    pass

            # If our satisfying type is any, we can return the data as is.
            if satisfying_type is Any:
                return field_value

        # The value is not none. If it is a type in the field types, return it.
        raise ValueError()

    @classmethod
    def _deserialize_field(cls, serialized_value: Any, field_type: Type) -> Any:
        # Obtain type information.
        origin_type, origin_type_args = _get_potential_types(field_type)

        # Obtain a list of types that satisfy this field. If this is a union, it's arguments are our satisfying types.
        satisfying_types: List[Type] = []
        if origin_type is Union:
            satisfying_types.extend(origin_type_args)
        else:
            satisfying_types.append(field_type)

        # If the value is None and we allow None types, return it. Otherwise throw an error.
        if serialized_value is None:
            if type(None) in satisfying_types or Any in satisfying_types:
                return None
            else:
                raise ValueError("Error deserializing field. Expected a non-None type, but got None")

        # It can't be a none type now, so remove it from our list of potential types
        if type(None) in satisfying_types:
            satisfying_types.remove(type(None))

        # Loop through all our satisfying types.
        for satisfying_type in satisfying_types:

            # If our satisfying type is any, we can return the data as is.
            if satisfying_type is Any:
                return serialized_value

            # Some satisfying types will be classes, these are typical object types.
            # Otherwise, they will be typing.* objects that we resolve in special cases below.
            if inspect.isclass(satisfying_type):
                # Handle ints
                if satisfying_type is int and isinstance(serialized_value, int) or \
                        satisfying_type is str and isinstance(serialized_value, str) or \
                        satisfying_type is float and isinstance(serialized_value, float) or \
                        satisfying_type is bool and isinstance(serialized_value, bool):
                    return serialized_value

                # Handle enums
                if issubclass(satisfying_type, IntEnum) and isinstance(serialized_value, int):
                    return satisfying_type(serialized_value)
                if issubclass(satisfying_type, Enum) and isinstance(serialized_value, str):
                    return satisfying_type(serialized_value)

                # If our current satisfying type is a serializable structure and we have a dict, try to deserialize
                # with it.
                if issubclass(satisfying_type, SerializableStructure) and isinstance(serialized_value, dict):
                    try:
                        deserialized_value = satisfying_type.from_dict(serialized_value)
                        return deserialized_value
                    except ValueError:
                        pass

            # Handle lists if our serialized value is a list
            if isinstance(serialized_value, list):
                try:
                    # Obtain information about the satisfying type
                    if inspect.isclass(satisfying_type) and satisfying_type is list:
                        potential_list_origin_type = list
                        potential_list_element_types = []
                    else:
                        potential_list_origin_type, potential_list_element_types = _get_potential_types(satisfying_type)

                    if potential_list_origin_type is not None and issubclass(potential_list_origin_type, list):
                        # Obtain our element type. If we don't have one, we use 'Any' by default
                        element_type = Any
                        if len(potential_list_element_types) > 0:
                            element_type = potential_list_element_types[0]

                        # Deserialize the list accordingly.
                        deserialized_list = [
                            cls._deserialize_field(serialized_element, element_type)
                            for serialized_element in serialized_value
                        ]
                        return deserialized_list
                except ValueError:
                    pass

        # The value is not none. If it is a type in the field types, return it.
        raise ValueError()

    @classmethod
    def from_dict(cls, obj: dict) -> 'SerializableStructure':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        # Create our initialization arguments.
        init_args: dict = {}

        # Obtain the fields for this item
        fields_list = fields(cls)

        # Loop for each field to populate it
        for field in fields_list:
            # Obtain field information
            serialized_field_name: str = field.name
            field_metadata: dict = field.metadata

            # If we have a name override, we use that name
            name_override = field_metadata.get('name')
            if name_override is not None:
                serialized_field_name = name_override
            else:
                # If we don't have an override, we convert to camel case
                serialized_field_name = _to_camel_case(serialized_field_name)

            # Obtain our serialized value
            serialized_field_value = obj.get(serialized_field_name)

            # If this field existed in our object, deserialize it and set its value.
            if serialized_field_name in obj:
                # Deserialize the field value
                field_value = cls._deserialize_field(serialized_field_value, field.type)

                # If we are enforcing a constant, we raise an error if it does not match the default value.
                enforce_as_constant = field_metadata.get('enforce_as_constant')
                if enforce_as_constant:
                    default_value = _get_default_value(field)
                    if field_value != default_value:
                        raise ValueError(
                            f"Field {field.name} could not be deserialized because metadata defined it as a constant "
                            f"and the provided value did not equal the default value."
                        )

                init_args[field.name] = field_value
            else:
                # Otherwise set the default value if we were provided one, otherwise we use None as a default.
                default_value = _get_default_value(field)
                init_args[field.name] = default_value

        # Use the parsed arguments to instantiate a copy of this class
        return cls(**init_args)

    def to_dict(self) -> dict:
        """
        Dumps an instance of this class to a dictionary object. It reads all relevant properties for this immediate
        class and classes it had inherited from.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create our resulting dictionary
        result = {}

        # Obtain the fields for this item
        fields_list: tuple = fields(self)

        # Loop for each field to populate it
        for field in fields_list:
            # Obtain field information
            serialized_field_name: str = field.name
            field_value: Any = getattr(self, field.name)
            field_metadata: dict = field.metadata

            # If we have a name override, we use that name
            name_override = field_metadata.get('name')
            if name_override is not None:
                serialized_field_name = name_override
            else:
                # If we don't have an override, we convert to camel case
                serialized_field_name = _to_camel_case(serialized_field_name)

            # If we are enforcing the default as a constant, we overwrite the field value with the default.
            enforce_as_constant = field_metadata.get('enforce_as_constant')
            if enforce_as_constant:
                field_value = _get_default_value(field)

            # Serialize this field
            serialized_field_value = self._serialize_field(field_value, field.type)

            # Determine if we should set the result. By default None is excluded, unless an override is provided
            include_none = field_metadata.get('include_none')
            if serialized_field_value is not None or include_none:
                result[serialized_field_name] = serialized_field_value

        return result
