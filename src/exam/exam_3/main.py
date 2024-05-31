import argparse
from typing import Any

from src.exam.exam_3.path_finder import *


def parse_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", type=str, nargs="+")
    parser.add_argument("processor_count", type=int)
    parser.add_argument("--unique", action="store_true")
    args = parser.parse_args()

    return vars(args)


def get_path_between_two(
    result_path: list[str], start_page: str, end_page: str, processor_cnt: int, unique: bool
) -> Optional[list[str]]:
    start_page = f"https://en.wikipedia.org/wiki/{start_page}"
    end_page = f"https://en.wikipedia.org/wiki/{end_page}"

    return multiprocess_find_path(result_path, start_page, end_page, processor_cnt, unique)


def get_all_path(pages: list[str], processor_cnt: int, unique: bool = False) -> None:
    if unique and len(pages) > len(set(pages)):
        print("There should not be identical pages in your link list")
    else:
        output: list[str] = []
        for i in range(len(pages) - 1):
            get_path_between_two(output, pages[i], pages[i + 1], processor_cnt, unique)

        output.append(f"https://en.wikipedia.org/wiki/{pages[-1]}")
        number = 1
        print(output)
        print("\nThe final path found is:")
        for link in output:
            print(f"{number}) {link}")
        number += 1


if __name__ == "__main__":
    args = parse_args()
    get_all_path(*args.values())
