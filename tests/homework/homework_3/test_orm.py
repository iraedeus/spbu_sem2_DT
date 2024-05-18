from dataclasses import dataclass

import pytest

from src.homework.homework_3.orm import ORM, IncompatibleData


@dataclass
class TestFirst(ORM):
    name: str
    login: str
    is_authorized: bool


@dataclass
class TestNested(ORM):
    ggwp: bool
    csgo: int


@dataclass
class TestSecond(ORM):
    name: str
    game: TestNested


def create_obj(cls, asdict_obj, strict=False):
    obj = cls.from_dict(asdict_obj, strict)
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
        expected = TestFirst(None, None, None)
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
