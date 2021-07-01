from dataclasses import dataclass, field
from typing import Optional, List, Union, Dict

from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure, serialization_metadata


@dataclass
class TestClassA(SerializableStructure):
    num: int


@dataclass
class TestClassB(TestClassA):
    num2: int

@dataclass
class TestComplexTypeHints(SerializableStructure):
    super_union: Union[bool, Union[str, str, bool, Union[TestClassA, None], None], None]
    statuses: List[bool]
    texts: List[str]
    ids: List[Union[str, int]]
    commands: Union[str, List[str]]
    test: List[List[List[List[str]]]]
    bool_with_override: bool = field(
        default=False,
        metadata=serialization_metadata(name_override="SPECIAL_NAME_BOOL")
    )
    test_basic_list: Optional[list] = None
    test_basic_list2: list = field(default_factory=list)
    excluded_null: Optional[str] = None
    included_null: Optional[str] = field(default=None, metadata=serialization_metadata(include_none=True))
    constant_test: str = field(default='CONSTANT_VALUE', metadata=serialization_metadata(enforce_as_constant=True))


# Create a basic structure
testComplexTypeHints = TestComplexTypeHints(
    super_union=TestClassA(0),
    statuses=[True, True, False, True],
    texts=["ok", "OK"],
    ids=["id1", 2, "id3", 4],
    commands=["cmd", "-c", "echo hi"],
    test=[[], [[[]]], [[["hi", "ok"]]]],
    test_basic_list=["ok", "ok2", "ok3", 7, [7, 8, 9]],
    test_basic_list2=["ok4", "ok5", "ok6", 1, [2, 3, 4]],
)


def test_basic_inheritance():
    b = TestClassB(0, 7)
    result = b.to_dict()
    assert 'num' in result and 'num2' in result
    b_copy = TestClassB.from_dict(b.to_dict())
    assert b.num == b_copy.num and b.num2 == b_copy.num2


def test_deserialization():
    # Serialize testComplexTypeHints
    serialized = testComplexTypeHints.to_dict()

    # Verify our included/excluded null values are/aren't there, as expected.
    assert 'includedNull' in serialized
    assert 'excludedNull' not in serialized

    # Verify round trip serialization
    b_copy = TestComplexTypeHints.from_dict(serialized)
    assert testComplexTypeHints == b_copy


def test_name_override():
    # Serialize testComplexTypeHints
    serialized = testComplexTypeHints.to_dict()

    # Verify our name override is valid
    assert 'SPECIAL_NAME_BOOL' in serialized


def test_enforce_as_constant():
    # Serialize testComplexTypeHints
    serialized = testComplexTypeHints.to_dict()

    # Set a bad value for the constant in the dictionary and try to deserialize.
    failed_bad_constant = False
    try:
        serialized['constantTest'] = 'BAD_CONSTANT_VALUE'
        b_failed_example = TestComplexTypeHints.from_dict(serialized)
    except ValueError:
        failed_bad_constant = True
    assert failed_bad_constant


@dataclass
class TestDictStruct(SerializableStructure):
    x: int
    y: TestClassA
    z: Dict[str, TestClassA]


def test_struct_with_dict():
    # Create a test structure with a dictionary
    test_dict = TestDictStruct(
        x=0,
        y=TestClassA(7),
        z={
            "first": TestClassA(1),
            "second": TestClassA(2)
        }
    )

    # Serialize our structure
    serialized = test_dict.to_dict()

    # Verify round trip serialization
    test_dict_copy = TestDictStruct.from_dict(serialized)
    assert test_dict == test_dict_copy
