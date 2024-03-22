from typing import Callable, Generic, Optional, Type, TypeVar

Parent = TypeVar("Parent")


class AlreadyExistError(Exception):
    pass


class Registry(Generic[Parent]):
    def __init__(self, default: Optional[Type[Parent]]) -> None:
        self.classes: dict[str, Type[Parent]] = dict()
        self.default: Optional[Type[Parent]] = default

    def register(self, name: str) -> Callable[[Type[Parent]], Type[Parent]]:
        def inner(cls: Type[Parent]) -> Type[Parent]:
            if name not in self.classes:
                self.classes[name] = cls
                return cls
            else:
                raise AlreadyExistError("This name of class already exist in registry")

        return inner

    def dispatch(self, name: str) -> Type[Parent]:
        if name in self.classes:
            return self.classes[name]
        elif self.default is not None:
            return self.default
        else:
            raise ValueError("This class is unknown")


class ParentClass:
    pass


parent = Registry[ParentClass](default=None)


@parent.register(name="AVL")
class AVLTree(ParentClass):
    pass


@parent.register(name="Treap")
class CartesianTree(ParentClass):
    pass


@parent.register(name="Smh")
class SomethingElse(ParentClass):
    pass


if __name__ == "__main__":
    user_choice = input("Select the class whose object you want to create: \n" "Available: AVL, Treap, Smh \n")

    user_class = parent.dispatch(user_choice)
    print(user_class())
