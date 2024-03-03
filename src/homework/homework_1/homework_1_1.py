from typing import Callable, Generic, Optional, TypeVar


class Mapping:
    pass


Parent = TypeVar("Parent")


class Registry(Generic[Parent]):
    def __init__(self, default: Callable = None) -> None:
        self.classes: dict[str, "Parent"] = {}
        self.default = default

    def register(self, name: str) -> Callable:
        def inner(registered_class: Parent) -> Parent:
            self.classes[name] = registered_class
            return registered_class

        return inner

    def dispatch(self, name: str) -> Optional[Parent] | Callable:
        if name in self.classes:
            return self.classes[name]
        elif self.default is not None:
            return self.default

        if name not in self.classes:
            raise ValueError("This class is unknown")


mapping = Registry[Mapping](default=dict)


@mapping.register(name="AVL")
class AVLTree(Mapping):
    pass
