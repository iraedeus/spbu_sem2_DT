from typing import Any, Optional, Type, TypeVar, get_args

from src.homework.homework_3.json_parser import parse_json

T = TypeVar("T", bound="ORM")


class IncompatibleData(Exception):
    pass


class Descriptor(object):
    def __init__(self, label: str) -> None:
        self._label = label
        self._value = None

    def __set__(self, instance: T, value: Any) -> None:
        instance.__dict__[self._label] = value

    def __get__(self, instance: T, owner: Type[T]) -> Optional[Any]:
        if not hasattr(instance, "dict"):
            raise AttributeError

        attr_name = self._label
        if attr_name not in instance.dict.keys():
            raise AttributeError(f"The object does not have an attribute with a name {attr_name}")

        if not self._value:
            self._value = instance.__dict__[attr_name]

        value = self._value

        if value:
            return value
        elif value is None and attr_name in instance.dict.keys():
            new_value = instance.dict[attr_name]
            if isinstance(new_value, dict):
                sub_cls = instance.__annotations__[self._label]
                sub_instance = sub_cls.from_dict(new_value)
                setattr(instance, attr_name, sub_instance)
                return sub_instance
            if isinstance(new_value, list) and len(new_value) != 0 and isinstance(new_value[0], dict):
                sub_cls = get_args(instance.__annotations__[self._label])[0]
                list_obj = [sub_cls.from_dict(dict_obj) for dict_obj in new_value]
                setattr(instance, attr_name, list_obj)
                return instance.__dict__[attr_name]
            else:
                setattr(instance, attr_name, new_value)
                return instance.__dict__[attr_name]
        else:
            return value


class ORM:
    @classmethod
    def from_dict(cls: Type[T], asdict_obj: dict[str, Any], strict: bool = False) -> T:
        cls.set_descr(asdict_obj, strict)
        datacls_attrs = cls.__annotations__.keys()
        actual_attrs = asdict_obj.keys()
        arr = [None] * len(datacls_attrs)
        instance = cls(*arr)
        setattr(instance, "dict", asdict_obj)

        if not strict:
            for name in actual_attrs:
                if name not in datacls_attrs:
                    setattr(instance, name, None)

        return instance

    @classmethod
    def set_descr(cls: Type[T], asdict_obj: dict[str, Any], strict: bool = False) -> None:
        datacls_attrs = cls.__annotations__.keys()
        actual_attrs = asdict_obj.keys()

        if strict:
            if datacls_attrs == actual_attrs:
                for name in datacls_attrs:
                    setattr(cls, name, Descriptor(name))
            else:
                raise IncompatibleData(
                    "The data from the JSON file does not match the expected structure in strict mode."
                )
        else:
            iter_attrs = list(set().union(datacls_attrs, actual_attrs))
            for name in iter_attrs:
                setattr(cls, name, Descriptor(name))


if __name__ == "__main__":
    pass
