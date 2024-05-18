from __future__ import annotations

import json
from dataclasses import asdict
from json import JSONDecodeError
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

T = TypeVar("T")


def parse_json(fp: str) -> dict:
    with open(fp, "r") as json_file:
        try:
            return json.load(json_file)
        except JSONDecodeError:
            return {}


def dataclass_dump(obj: DataclassInstance, fp: str) -> None:
    obj_dict = asdict(obj)
    with open(fp, "w+") as json_file:
        json.dump(obj_dict, json_file)
        json_file.write("\n")


if __name__ == "__main__":
    pass
