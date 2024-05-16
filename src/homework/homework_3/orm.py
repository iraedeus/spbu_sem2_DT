from typing import Any, Optional, Type, TypeVar, get_args

from src.homework.homework_3.json_parser import parse_json

T = TypeVar("T", bound="ORM")


class IncompatibleData(Exception):
    pass


class Descr(object):
    def __init__(self, label: str) -> None:
        self._label = label

    def __set__(self, instance: T, value: Any) -> None:
        instance.__dict__[self._label] = value

    def __get__(self, instance: T, owner: Type[T]) -> Optional[Any]:
        if not hasattr(instance, "dict"):
            raise AttributeError
        attr_name = self._label
        value = instance.__dict__[attr_name]

        if value:
            return value
        elif value is None and attr_name in instance.dict.keys():
            new_value = instance.dict.get(attr_name)
            setattr(instance, attr_name, new_value)
            return instance.__dict__[attr_name]
        else:
            return value


class ORM:
    @classmethod
    def from_dict(cls: Type[T], asdict_obj: dict[str, Any], strict: bool = False) -> T:
        def recursion(cls: Type[T], asdict_obj: dict[str, Any]) -> T:
            new_cls = cls.set_descr(asdict_obj, strict)
            instance = new_cls()
            setattr(instance, "dict", asdict_obj)
            datacls_attrs = new_cls.__annotations__.keys()
            actual_attrs = asdict_obj.keys()

            for name in actual_attrs:
                curr_obj = asdict_obj[name]
                if isinstance(curr_obj, dict):
                    try:
                        sub_cls = instance.__annotations__[name]
                    except KeyError:
                        continue

                    setattr(instance, name, recursion(sub_cls, curr_obj))
                elif (isinstance(curr_obj, list) and len(curr_obj) != 0) and isinstance(curr_obj[0], dict):
                    try:
                        sub_cls = get_args(instance.__annotations__[name])
                        objects = [recursion(sub_cls[0], obj) for obj in curr_obj]
                        setattr(instance, name, objects)
                    except KeyError:
                        continue

            if not strict:
                for name in actual_attrs:
                    if name not in datacls_attrs:
                        setattr(instance, name, None)
            return instance

        return recursion(cls, asdict_obj)

    @classmethod
    def set_descr(cls: Type[T], asdict_obj: dict[str, Any], strict: bool = False) -> Type[T]:
        datacls_attrs = cls.__annotations__.keys()
        actual_attrs = asdict_obj.keys()

        if strict:
            if datacls_attrs == actual_attrs:
                for name in datacls_attrs:
                    setattr(cls, name, Descr(name))
            else:
                raise IncompatibleData(
                    "The data from the JSON file does not match the expected structure in strict mode."
                )
        else:
            for name in actual_attrs:
                setattr(cls, name, Descr(name))

        return cls


if __name__ == "__main__":
    pass
