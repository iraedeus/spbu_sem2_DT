from io import StringIO

import hypothesis.strategies as st
import pytest
from hypothesis import assume
from hypothesis.stateful import Bundle, RuleBasedStateMachine, invariant, rule

from src.homework.homework_2.actions import *


def create_test_cmd_storage(storage):
    new_stack = Stack(None)
    return PerformedCommandStorage(storage=storage, history=new_stack)


def parse(fake_data):
    lines = fake_data.split("")


class StackTest(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()

    database = Stack(None)
    compared_database = []
    values = Bundle("values")

    @rule(target=values, v=st.integers())
    def add_value(self, v):
        return v

    @rule(v=values)
    def put_to_database(self, v):
        self.database.put(v)
        self.compared_database.append(v)

    @rule()
    def pop_from_database(self):
        if len(self.compared_database) > 1:
            self.database.pop()
            del self.compared_database[-1]

    @invariant()
    def compare(self):
        if len(self.compared_database) != 0:
            assert self.compared_database[-1] == self.database.head.value


class TestCommandStorage:
    @pytest.mark.parametrize("storage", [({1, 2, 5}), ({111, 5})])
    def test_err_not_indexed(self, storage):
        with pytest.raises(TypeError):
            cmd_storage = create_test_cmd_storage(storage)

    @pytest.mark.parametrize("storage", [([1, 2, 5]), ([111, 5])])
    def test_err_empty_history(self, storage):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.undo()


class TestActionInsertFirst:
    @pytest.mark.parametrize(
        "storage, value, expected",
        [([1, 5, 4, 3], 8, [8, 1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 10, [10, 1, 5, 4, 6, 7, 8, 3])],
    )
    def test_do(self, storage, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertFirst(value))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, value_1, value_2, expected",
        [([1, 5, 4, 3], 8, 9, [8, 1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 10, 11, [10, 1, 5, 4, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, value_1, value_2, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertFirst(value_1))
        cmd_storage.apply(action=ActionInsertFirst(value_2))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, value", [([1, 2, 5], "ggwp"), ([111, 5], (5, 6))])
    def test_err_not_int(self, storage, value):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(TypeError):
            cmd_storage.apply(ActionInsertFirst(value))


class TestActionInsertLast:
    @pytest.mark.parametrize(
        "storage, value, expected",
        [([1, 5, 4, 3], 8, [1, 5, 4, 3, 8]), ([1, 5, 4, 6, 7, 8, 3], 10, [1, 5, 4, 6, 7, 8, 3, 10])],
    )
    def test_do(self, storage, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertLast(value))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, value_1, value_2, expected",
        [([1, 5, 4, 3], 8, 9, [1, 5, 4, 3, 8]), ([1, 5, 4, 6, 7, 8, 3], 10, 11, [1, 5, 4, 6, 7, 8, 3, 10])],
    )
    def test_undo(self, storage, value_1, value_2, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertLast(value_1))
        cmd_storage.apply(action=ActionInsertLast(value_2))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, value", [([1, 2, 5], "ggwp"), ([111, 5], (5, 6))])
    def test_err_not_int(self, storage, value):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(TypeError):
            cmd_storage.apply(ActionInsertFirst(value))


class TestActionSwap:
    @pytest.mark.parametrize(
        "storage, first_index, second_index, expected",
        [([1, 5, 4, 3], 0, 1, [5, 1, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 0, 4, [7, 5, 4, 6, 1, 8, 3])],
    )
    def test_do(self, storage, first_index, second_index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionSwap(first_index, second_index))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, first_index, second_index, expected",
        [([1, 5, 4, 3], 0, 2, [4, 5, 1, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, 5, [1, 5, 8, 6, 7, 4, 3])],
    )
    def test_undo(self, storage, first_index, second_index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionSwap(first_index, second_index))
        cmd_storage.apply(action=ActionSwap(first_index + 1, second_index + 1))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, first_index, second_index", [([1, 2, 3], 0, 100), ([111, 5], 101, 100)])
    def test_err_no_index(self, storage, first_index, second_index):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionSwap(first_index, second_index))


class TestActionAdd:
    @pytest.mark.parametrize(
        "storage, index, value, expected",
        [([1, 5, 4, 3], 0, 5, [6, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 5, 4, [1, 5, 4, 6, 7, 12, 3])],
    )
    def test_do(self, storage, index, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionAdd(index, value))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, index, value, expected",
        [([1, 5, 4, 3], 1, 4, [1, 9, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, 5, [1, 5, 9, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, index, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionAdd(index, value))
        cmd_storage.apply(action=ActionAdd(index, value))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, index, value", [([1, 2, 3], 100, 100), ([111, 5], 101, 100)])
    def test_err_no_index(self, storage, index, value):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionAdd(index, value))


class TestActionFlip:
    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 0, [-1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 5, [1, 5, 4, 6, 7, -8, 3])],
    )
    def test_do(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionFlip(index))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 1, [1, -5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, [1, 5, -4, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionFlip(index))
        cmd_storage.apply(action=ActionFlip(index))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, index", [([1, 2, 3], 100), ([111, 5], 101)])
    def test_err_no_index(self, storage, index):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionFlip(index))


class TestActionSquare:
    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 0, [1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 5, [1, 5, 4, 6, 7, 64, 3])],
    )
    def test_do(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionSquare(index))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 1, [1, 25, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, [1, 5, 16, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionSquare(index))
        cmd_storage.apply(action=ActionSquare(index))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, index", [([1, 2, 3], 100), ([111, 5], 101)])
    def test_err_no_index(self, storage, index):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionSquare(index))


class TestActionDeleteSlice:
    @pytest.mark.parametrize(
        "storage, first_index, second_index, expected",
        [([1, 5, 4, 3], 0, 1, [4, 3]), ([1, 5, 4, 6, 7, 8, 3], 0, 4, [8, 3])],
    )
    def test_do(self, storage, first_index, second_index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionDeleteSlice(first_index, second_index))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, first_index, second_index, expected",
        [([1, 5, 4, 3], 0, 2, [1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, 5, [1, 5, 4, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, first_index, second_index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionDeleteSlice(first_index, second_index))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, first_index, second_index", [([1, 2, 3], 0, 100), ([111, 5], 1, 0)])
    def test_err_no_index(self, storage, first_index, second_index):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionDeleteSlice(first_index, second_index))


class TestActionPop:
    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 0, [5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 5, [1, 5, 4, 6, 7, 3])],
    )
    def test_do(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionPop(index))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 1, [1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, [1, 5, 4, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionPop(index))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, index", [([1, 2, 3], 100), ([111, 5], 101)])
    def test_err_no_index(self, storage, index):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionSquare(index))


class TestActionMove:
    @pytest.mark.parametrize(
        "storage, step, expected",
        [([1, 5, 4, 3], 0, [1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 5, [4, 6, 7, 8, 3, 1, 5])],
    )
    def test_do(self, storage, step, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionMove(step))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, step, expected",
        [([1, 5, 4, 3], 1, [3, 1, 5, 4]), ([1, 5, 4, 6, 7, 8, 3], 2, [8, 3, 1, 5, 4, 6, 7])],
    )
    def test_undo(self, storage, step, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionMove(step))
        cmd_storage.apply(action=ActionMove(step))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, step", [([1, 2, 3], 100), ([111, 5], 101)])
    def test_err_no_index(self, storage, step):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionSquare(step))


def get_output(string: str):
    strings = string.split("\n")
    return eval(strings[-2])


@pytest.mark.parametrize(
    "actions, expected",
    [
        (
            [
                "InsertFirst 1",
                "InsertFirst 2",
                "InsertLast 3",
                "InsertLast 4",
                "Reverse",
                "Move 1",
                "Pop 0",
                "Show",
                "Exit",
            ],
            [4, 3, 1],
        ),
        (["InsertFirst 100", "InsertLast 500", "Square 0", "Undo", "Show", "Exit"], [100, 500]),
        (["InsertFirst 100", "InsertLast 10000", "Undo", "Undo", "Show", "Exit"], []),
    ],
)
def test_main_scenario(actions, expected, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: actions.pop(0))
    main()
    captured = capsys.readouterr().out

    assert get_output(captured) == expected


@pytest.mark.parametrize(
    "actions, expected_err",
    [
        (
            ["InsertFirst 1", "InsertFirst 2", "InsertLast 3", "InsertLast 4", "Reverse", "Move 1", "Pop 100", "Exit"],
            "pop index out of range",
        ),
        (
            ["InsertFirst 100", "InsertLast 500", "Square 0", "Undo", "Undo", "Undo", "Undo", "Exit"],
            "No action in history",
        ),
        (["InsertFirst 100", "InsertLast [][", "Exit"], "Your arguments must be integer"),
    ],
)
def test_main_scenario_err(actions, expected_err, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: actions.pop(0))
    main()
    captured = capsys.readouterr().out

    assert captured.split("\n")[-2] == expected_err


StackTestCase = StackTest.TestCase
