import inspect
from abc import ABCMeta, abstractmethod
from collections import deque
from typing import Any, Optional

from src.homework.homework_1.registry import *

ACTIONS = Registry["Action"](default=None)


class PerformedCommandStorage:
    def __init__(self, storage: list[int], history: deque = deque()) -> None:
        if not isinstance(storage, list):
            raise TypeError("Storage must be list")
        self.history: deque = history
        self.storage: list[int] = storage

    def apply(self, action: "Action") -> None:
        action.do(self.storage)
        self.history.append(action)

    def undo(self) -> None:
        action = self.history.pop()
        action.undo(self.storage)


class Action(metaclass=ABCMeta):
    def __init__(self, *args: Any) -> None:
        pass

    @abstractmethod
    def do(self, storage_list: list[int]) -> None:
        pass

    @abstractmethod
    def undo(self, storage_list: list[int]) -> None:
        pass


@ACTIONS.register("InsertFirst")
class ActionInsertFirst(Action):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("The type of the value must be an int")
        self.value = value

    def do(self, storage_list: list[int]) -> None:
        storage_list.insert(0, self.value)

    def undo(self, storage_list: list[int]) -> None:
        del storage_list[0]


@ACTIONS.register("InsertLast")
class ActionInsertLast(Action):
    def __init__(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The type of the value must be an int")
        self.value = value

    def do(self, storage_list: list[int]) -> None:
        storage_list.append(self.value)

    def undo(self, storage_list: list[int]) -> None:
        del storage_list[-1]


@ACTIONS.register("Swap")
class ActionSwap(Action):
    def __init__(self, first_index: int, second_index: int):
        if not isinstance(first_index, int) or not isinstance(second_index, int):
            raise TypeError("The type of the indexes must be an int")
        self.first_index = first_index
        self.second_index = second_index

    def do(self, storage_list: list[int]) -> None:
        storage_list[self.first_index], storage_list[self.second_index] = (
            storage_list[self.second_index],
            storage_list[self.first_index],
        )

    def undo(self, storage_list: list[int]) -> None:
        self.do(storage_list)


@ACTIONS.register("Add")
class ActionAdd(Action):
    def __init__(self, index: int, value: int):
        if not isinstance(value, int) or not isinstance(index, int):
            raise TypeError("The type of the value and index must be an int")
        self.index = index
        self.value = value

    def do(self, storage_list: list[int]) -> None:
        storage_list[self.index] += self.value

    def undo(self, storage_list: list[int]) -> None:
        storage_list[self.index] -= self.value


@ACTIONS.register("Flip")
class ActionFlip(Action):
    def __init__(self, index: int) -> None:
        self.index = index

    def do(self, storage_list: list[int]) -> None:
        storage_list[self.index] = -storage_list[self.index]

    def undo(self, storage_list: list[int]) -> None:
        self.do(storage_list)


@ACTIONS.register("Square")
class ActionSquare(Action):
    def __init__(self, index: int) -> None:
        self.index = index

    def do(self, storage_list: list[int]) -> None:
        storage_list[self.index] = storage_list[self.index] ** 2

    def undo(self, storage_list: list[int]) -> None:
        storage_list[self.index] = int(storage_list[self.index] ** 0.5)


@ACTIONS.register("Reverse")
class ActionReverse(Action):
    def __init__(self) -> None:
        pass

    def do(self, storage_list: list[int]) -> None:
        storage_list.reverse()

    def undo(self, storage_list: list[int]) -> None:
        storage_list.reverse()


@ACTIONS.register("DeleteSlice")
class ActionDeleteSlice(Action):
    def __init__(self, first_index: int, second_index: int) -> None:
        if not isinstance(first_index, int) or not isinstance(second_index, int):
            raise TypeError("The type of the indexes must be an int")

        self.first_index: int = first_index
        self.second_index: int = second_index
        self.deleted_slice: list[int] = []

    def do(self, storage_list: list[int]) -> None:
        if not ((0 <= self.first_index < len(storage_list)) and (0 <= self.second_index < len(storage_list))):
            raise IndexError("Index out of range")
        if self.first_index > self.second_index:
            raise IndexError("First index must be less or equal then second index")

        self.deleted_slice = storage_list[self.first_index : self.second_index + 1]
        del storage_list[self.first_index : self.second_index + 1]

    def undo(self, storage_list: list[int]) -> None:
        storage_list[: self.first_index] += self.deleted_slice


@ACTIONS.register("Pop")
class ActionPop(Action):
    def __init__(self, index: int) -> None:
        self.index = index
        self.value: int

    def do(self, storage_list: list[int]) -> None:
        self.value = storage_list.pop(self.index)

    def undo(self, storage_list: list[int]) -> None:
        storage_list.insert(self.index, self.value)


@ACTIONS.register("Move")
class ActionMove(Action):
    def __init__(self, step: int) -> None:
        self.step = step

    def do(self, storage_list: list[int]) -> None:
        if self.step == 0:
            return None

        length = len(storage_list)
        storage_list[length - self.step :] += storage_list[: length - self.step]
        del storage_list[: length - self.step]

    def undo(self, storage_list: list[int]) -> None:
        if self.step == 0:
            return None

        self.step = len(storage_list) - self.step
        self.do(storage_list)


def parse_args(user_command: str) -> tuple[str, list[Any]]:
    action, *args = user_command.split(" ")
    return action, args


def to_int(args: list[Any]) -> list[int]:
    return list(map(int, args))


def do_action(user_cmd_storage: PerformedCommandStorage, user_action: str, args: list[Any]) -> None:
    if user_action == "Undo":
        try:
            return user_cmd_storage.undo()
        except IndexError:
            print("No action in history")
            return None

    try:
        action = ACTIONS.dispatch(user_action)
    except ValueError:
        print("Unknown command")
        return None

    try:
        args = to_int(args)
    except ValueError:
        print("Your arguments must be integer")
        return None

    try:
        user_cmd_storage.apply(action(*args))
    except IndexError as error:
        print(error)


def create_start_message() -> str:
    def get_args(cls: Type[T]) -> str:
        args = ""
        arg_names = inspect.getfullargspec(cls.__init__)[0]
        for name in arg_names[2:]:
            args += f"--{name} "
        return args

    msg = "This is a program for performing actions on a list of integers. Available commands: \n"
    number = 1

    for action_name, action_cls in ACTIONS.classes.items():
        msg += f"{number}) {action_name} {get_args(action_cls)}\n"
        number += 1

    msg += f"{number + 1}) Show (Print your list in console)\n"
    msg += f"{number + 2}) Exit (Exit the program)"

    return msg


def main() -> None:
    print(create_start_message())
    user_cmd_storage = PerformedCommandStorage([], deque())
    while True:
        user_command = input("Enter your command with args: \n")
        user_action, args = parse_args(user_command)

        if user_action == "Exit":
            break
        elif user_action == "Show":
            print(user_cmd_storage.storage)
        else:
            do_action(user_cmd_storage, user_action, args)


if __name__ == "__main__":
    main()
