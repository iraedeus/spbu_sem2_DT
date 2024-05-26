from typing import Any, Callable, Generic, Optional, TypeVar

T2ANY_CALLABLE = Callable


class Observable:
    def __init__(self, initial: int) -> None:
        self._value = initial
        self.callbacks: list[T2ANY_CALLABLE] = []

    def add_callback(self, func: T2ANY_CALLABLE) -> None:
        self.callbacks.append(func)

    def _do_callbacks(self) -> None:
        for func in self.callbacks:
            func(self.value)

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        self._value = new_value
        self._do_callbacks()

    @value.deleter
    def value(self) -> None:
        self._value = -1
        self._do_callbacks()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Observable):
            return NotImplemented
        return self.value == other.value
