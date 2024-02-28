import pytest

from src.homework_1.homework_1_1 import *

dummy_mapping = Registry[Mapping](default=dict)
dummy_mapping_for_errors = Registry[Mapping]()


@dummy_mapping_for_errors.register(name="sussy_dummy")
@dummy_mapping.register(name="dummy")
class Dummy(Mapping):
    pass


@pytest.mark.parametrize("name, class_check", [("dummy", Dummy), ("unknown", dict)])
def test_dispatch(name, class_check):
    test1 = dummy_mapping.dispatch(name)()
    assert isinstance(test1, class_check)


def test_dispatch_err():
    with pytest.raises(ValueError):
        test1 = dummy_mapping_for_errors.dispatch("unknown class")()
