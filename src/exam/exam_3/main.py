import argparse
from typing import Any

from src.exam.exam_3.path_finder import *


def parse_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("depth", help="Count of pages in path", type=int)
    parser.add_argument("processor_count", type=int)
    parser.add_argument("-page_name", type=str)
    args = parser.parse_args()

    return vars(args)


def get_path(depth: int, processor_count: int, page_name: str = "Adolf_Hitler") -> None:
    if page_name is None:
        actual_name = get_name_of_page()
        page_name = actual_name.replace(" ", "_")

    init_page = f"https://en.wikipedia.org/wiki/{page_name}"

    path = multiprocess_path_finder(depth, processor_count, init_page)
    if path[0] == "":
        print(f"There is no path with this depth from {page_name.split('/wiki/')}")
    else:
        print(f"Path from {page_name.split('/wiki/')[-1]} to Adolf Hitler is:")
        for page in path:
            print(page)


if __name__ == "__main__":
    args = parse_args()
    get_path(*args.values())
