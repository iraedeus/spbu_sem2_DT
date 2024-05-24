from typing import Any, Callable, Generic, Optional, TypeVar

T = TypeVar("T")
T2ANY_CALLABLE = Callable[[T], Any]


class Observable(Generic[T]):
    def __init__(self, initial: Optional[T] = None) -> None:
        self._value = initial
        self.callbacks: list[T2ANY_CALLABLE] = []

    def add_callback(self, func: T2ANY_CALLABLE):
        self.callbacks.append(func)

    def _do_callbacks(self) -> None:
        for func in self.callbacks:
            func(self.value)

    @property
    def value(self) -> Optional[T]:
        return self._value

    @value.setter
    def value(self, new_value: T):
        self._value = new_value
        self._do_callbacks()

    @value.deleter
    def value(self):
        self._value = None
        self._do_callbacks()
