import json
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from typing import Optional

import pytest

from src.homework.homework_3.json_parser import *
from src.homework.homework_3.orm import ORM, IncompatibleData


@dataclass
class TestFirst(ORM):
    name: Optional[str] = None
    login: Optional[str] = None
    is_authorized: Optional[bool] = None


@dataclass
class TestNested(ORM):
    ggwp: Optional[bool] = None
    csgo: Optional[int] = None


@dataclass
class TestSecond(ORM):
    name: Optional[str] = None
    game: TestNested = None


def create_obj(cls, asdict_obj, strict=False):
    with NamedTemporaryFile("r+") as json_file:
        data = json.dumps(asdict_obj)
        print(data)
        json_file.write(data)
        json_file.read()
        obj = cls.from_dict(json_file.name, strict)
        return obj


class TestORM:
    @pytest.mark.parametrize(
        "asdict_obj, keys, expected",
        [
            (
                {"name": "amogus", "login": "lays", "is_authorized": True},
                ["login"],
                {
                    "name": None,
                    "login": "lays",
                    "is_authorized": None,
                    "dict": {"name": "amogus", "login": "lays", "is_authorized": True},
                },
            ),
            (
                {"name": "amogus", "login": "lays", "is_authorized": True},
                ["login", "name"],
                {
                    "name": "amogus",
                    "login": "lays",
                    "is_authorized": None,
                    "dict": {"name": "amogus", "login": "lays", "is_authorized": True},
                },
            ),
        ],
    )
    def test_lazy_from_dict_no_wraps(self, asdict_obj, keys, expected):
        obj = create_obj(TestFirst, asdict_obj)
        [getattr(obj, key) for key in keys]
        assert obj.__dict__ == expected

    @pytest.mark.parametrize("asdict_obj", [({"name": "amogus", "login": "lays", "is_authorized": True})])
    def test_from_dict_no_wraps(self, asdict_obj):
        obj = create_obj(TestFirst, asdict_obj)
        expected = TestFirst()
        [setattr(expected, name, item) for name, item in asdict_obj.items()]
        setattr(expected, "dict", asdict_obj)
        assert obj == expected

    @pytest.mark.parametrize(
        "asdict_obj, keys, expected",
        [
            (
                {"name": "smh", "game": {"ggwp": True, "csgo": "yes"}},
                ["game", "ggwp"],
                {"ggwp": True, "csgo": None, "dict": {"ggwp": True, "csgo": "yes"}},
            )
        ],
    )
    def test_lazy_from_dict_with_wraps(self, asdict_obj, keys, expected):
        obj = create_obj(TestSecond, asdict_obj)
        nested_obj = getattr(obj, keys[0])
        getattr(nested_obj, keys[1])
        assert nested_obj.__dict__ == expected

    @pytest.mark.parametrize(
        "asdict_obj, key, expected",
        [({"name": "amogus", "login": "lays", "excess": True}, "excess", True)],
    )
    def test_not_strict_from_dict(self, asdict_obj, key, expected):
        obj = create_obj(TestFirst, asdict_obj)
        assert getattr(obj, key) == expected

    @pytest.mark.parametrize(
        "asdict_obj",
        [{"name": "amogus", "login": "lays", "excess": True}],
    )
    def test_strict_from_dict_err(self, asdict_obj):
        with pytest.raises(IncompatibleData):
            obj = create_obj(TestFirst, asdict_obj, True)
