import tempfile
from dataclasses import dataclass

import hypothesis.strategies as st
from hypothesis import given

from src.homework.homework_3.json_parser import *


@dataclass
class NestedDummy:
    smh: list[int]


@dataclass
class Dummy:
    amogus: int
    imposter: str
    another_dataclass: NestedDummy


def nested_strategy():
    return st.builds(NestedDummy, smh=st.lists(st.integers()))


def dummy_strategy():
    return st.builds(Dummy, amogus=st.integers(), imposter=st.text(), another_dataclass=nested_strategy())


@given(obj=dummy_strategy())
def test_dump(obj):
    dict_repr = asdict(obj)
    with tempfile.NamedTemporaryFile(mode="r+") as file:
        dataclass_dump(obj, f"{file.name}")
        assert dict_repr == json.load(file)
