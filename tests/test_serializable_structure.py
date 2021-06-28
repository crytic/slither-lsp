from dataclasses import dataclass
from typing import Optional

from slither_lsp.types.base_serializable_structure import SerializableStructure


@dataclass
class TestClassA(SerializableStructure):

    num: int

    def to_dict(self, result: Optional[dict] = None) -> dict:
        result['serializedNum'] = self.num

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        init_args['num'] = source_dict['serializedNum']

@dataclass
class TestClassB(TestClassA):
    num2: int

    def to_dict(self, result: Optional[dict] = None) -> dict:
        # Create a dictionary if we have none, serialize into it, and return the result.
        result: dict = result or {}
        TestClassA.to_dict(self, result)
        result['serializedNum2'] = self.num2
        return result

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        TestClassA._init_args_from_dict(init_args=init_args, source_dict=source_dict)
        init_args['num2'] = source_dict['serializedNum2']


def test_blah():
    b = TestClassB(0, 7)
    result = b.to_dict()
    assert 'serializedNum' in result and 'serializedNum2' in result
    b_copy = TestClassB.from_dict(b.to_dict())
    assert b.num == b_copy.num and b.num2 == b_copy.num2


def test_blah2():
    a = TestClassA(7)
    params = {
        'num': 7,
        'num2': 0
    }
    b = TestClassB(**params)
    assert b.num == 7 and b.num2 == 0
