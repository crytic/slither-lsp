from dataclasses import dataclass
from typing import Optional, List, Union

from slither_lsp.types.base_serializable_structure import SerializableStructure


@dataclass
class TestClassA(SerializableStructure):
    num: int


@dataclass
class TestClassB(TestClassA):
    num2: int


def test_basic_inheritance():
    b = TestClassB(0, 7)
    result = b.to_dict()
    assert 'num' in result and 'num2' in result
    b_copy = TestClassB.from_dict(b.to_dict())
    assert b.num == b_copy.num and b.num2 == b_copy.num2


@dataclass
class TestComplexTypeHints(SerializableStructure):
    super_union: Union[bool, Union[str, str, bool, Union[TestClassA, None], None], None]
    statuses: List[bool]
    texts: List[str]
    ids: List[Union[str, int]]
    commands: Union[str, List[str]]
    test: List[List[List[List[str]]]]


def test_deserialization():
    b = TestComplexTypeHints(
        super_union=TestClassA(0),
        statuses=[True, True, False, True],
        texts=["ok", "OK"],
        ids=["id1", 2, "id3", 4],
        commands=["cmd", "-c", "echo hi"],
        test=[[], [[[]]], [[["hi", "ok"]]]]
    )
    serialized = b.to_dict()
    b_copy = TestComplexTypeHints.from_dict(serialized)
    assert b == b_copy
