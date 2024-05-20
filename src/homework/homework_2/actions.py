import inspect
from typing import Any, Optional

from src.homework.homework_1.registry import *

ACTIONS = Registry["Action"](default=None)


class Node:
    def __init__(self, next: Optional["Node"], value: Any):
        self.next: Optional[Node] = next
        self.value = value


class Stack:
    def __init__(self, head: Optional[Node]) -> None:
        self.head: Optional[Node] = head

    def put(self, value: Any) -> None:
        new_node = Node(self.head, value)
        self.head = new_node

    def pop(self) -> Any:
        if self.head is None:
            raise IndexError("Pop from empty Stack object")

        value = self.head.value
        new_node = self.head.next
        self.head = new_node

        return value


class PerformedCommandStorage:
    def __init__(self, storage: list[int], history: Stack = Stack(None)) -> None:
        if not isinstance(storage, list):
            raise TypeError("Storage must be list")
        self.history: Stack = history
        self.storage: list[int] = storage

    def apply(self, action: "Action") -> None:
        action.do()
        self.history.put(action)

    def undo(self) -> None:
        if self.history.head is None:
            raise IndexError("Pop from empty Stack object")
        action = self.history.head.value
        action.undo()
        self.history.pop()


class Action:
    def __init__(self, *args: Any) -> None:
        pass

    def do(self) -> None:
        pass

    def undo(self) -> None:
        pass


@ACTIONS.register("InsertFirst")
class ActionInsertFirst(Action):
    def __init__(self, storage_list: list[int], value: int):
        if not isinstance(value, int):
            raise TypeError("The type of the value must be an int")
        self.value = value
        self.storage_list = storage_list

    def do(self) -> None:
        self.storage_list.insert(0, self.value)

    def undo(self) -> None:
        del self.storage_list[0]


@ACTIONS.register("InsertLast")
class ActionInsertLast(Action):
    def __init__(self, storage_list: list[int], value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The type of the value must be an int")
        self.value = value
        self.storage_list = storage_list

    def do(self) -> None:
        self.storage_list.append(self.value)

    def undo(self) -> None:
        del self.storage_list[-1]


@ACTIONS.register("Swap")
class ActionSwap(Action):
    def __init__(self, storage_list: list[int], first_index: int, second_index: int):
        if not isinstance(first_index, int) or not isinstance(second_index, int):
            raise TypeError("The type of the indexes must be an int")
        self.first_index = first_index
        self.second_index = second_index
        self.storage_list = storage_list

    def do(self) -> None:
        first_value, second_value = (
            self.storage_list[self.first_index],
            self.storage_list[self.second_index],
        )
        self.storage_list[self.first_index], self.storage_list[self.second_index] = (
            second_value,
            first_value,
        )

    def undo(self) -> None:
        self.do()


@ACTIONS.register("Add")
class ActionAdd(Action):
    def __init__(self, storage_list: list[int], index: int, value: int):
        if not isinstance(value, int) or not isinstance(index, int):
            raise TypeError("The type of the value and index must be an int")
        self.index = index
        self.value = value
        self.storage_list = storage_list

    def do(self) -> None:
        self.storage_list[self.index] += self.value

    def undo(self) -> None:
        self.storage_list[self.index] -= self.value


@ACTIONS.register("Flip")
class ActionFlip(Action):
    def __init__(self, storage_list: list[int], index: int) -> None:
        self.index = index
        self.storage_list = storage_list

    def do(self) -> None:
        self.storage_list[self.index] = -self.storage_list[self.index]

    def undo(self) -> None:
        self.do()


@ACTIONS.register("Square")
class ActionSquare(Action):
    def __init__(self, storage_list: list[int], index: int) -> None:
        self.index = index
        self.storage_list = storage_list

    def do(self) -> None:
        self.storage_list[self.index] = self.storage_list[self.index] ** 2

    def undo(self) -> None:
        self.storage_list[self.index] = int(self.storage_list[self.index] ** 0.5)


@ACTIONS.register("Reverse")
class ActionReverse(Action):
    def __init__(self, storage_list: list[int]):
        self.storage_list = storage_list

    def do(self) -> None:
        self.storage_list.reverse()

    def undo(self) -> None:
        self.storage_list.reverse()


@ACTIONS.register("DeleteSlice")
class ActionDeleteSlice(Action):
    def __init__(self, storage_list: list[int], first_index: int, second_index: int) -> None:
        if not isinstance(first_index, int) or not isinstance(second_index, int):
            raise TypeError("The type of the indexes must be an int")

        self.first_index: int = first_index
        self.second_index: int = second_index
        self.storage_list = storage_list
        self.deleted_slice: list[int] = []

    def do(self) -> None:
        if not ((0 <= self.first_index < len(self.storage_list)) and (0 <= self.second_index < len(self.storage_list))):
            raise IndexError("Index out of range")
        if self.first_index > self.second_index:
            raise IndexError("First index must be less or equal then second index")

        self.deleted_slice = self.storage_list[self.first_index : self.second_index + 1]
        del self.storage_list[self.first_index : self.second_index + 1]

    def undo(self) -> None:
        self.storage_list[: self.first_index] += self.deleted_slice


@ACTIONS.register("Pop")
class ActionPop(Action):
    def __init__(self, storage_list: list[int], index: int) -> None:
        self.index = index
        self.value: int
        self.storage_list = storage_list

    def do(self) -> None:
        self.value = self.storage_list.pop(self.index)

    def undo(self) -> None:
        self.storage_list.insert(self.index, self.value)


@ACTIONS.register("Move")
class ActionMove(Action):
    def __init__(self, storage_list: list[int], step: int) -> None:
        self.step = step
        self.storage_list = storage_list

    def do(self) -> None:
        if self.step == 0:
            return None

        length = len(self.storage_list)
        self.storage_list[length - self.step :] += self.storage_list[: length - self.step]
        del self.storage_list[: length - self.step]

    def undo(self) -> None:
        if self.step == 0:
            return None

        self.step = len(self.storage_list) - self.step
        self.do()


def parse_args(user_command: str) -> tuple[str, list[Any]]:
    strings = user_command.split(" ")
    return strings[0], strings[1:]


def to_int(args: list[Any]) -> list[int]:
    for i in range(len(args)):
        args[i] = int(args[i])

    return args


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
        user_cmd_storage.apply(action(user_cmd_storage.storage, *args))
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
    user_cmd_storage = PerformedCommandStorage([], Stack(None))
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
