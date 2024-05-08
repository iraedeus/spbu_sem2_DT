import json
from json import JSONDecodeError
from dataclasses import asdict
from typing import Callable, TypeVar

T = TypeVar("T")


def parse_json(fp: str) -> dict:
    with open(fp, "r") as json_file:
        try:
            return json.load(json_file)
        except JSONDecodeError:
            return {}


def dataclass_dump(cls: Callable, objects: list, fp: str) -> None:
    obj_dict = parse_json(fp)
    obj_dict[cls.__name__] = [asdict(obj) for obj in objects]
    with open(fp, "w+") as json_file:
        json.dump(obj_dict, json_file)
        json_file.write("\n")
