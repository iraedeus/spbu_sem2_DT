import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager, active_children, current_process
from multiprocessing.managers import BaseManager, DictProxy, ListProxy
from queue import Queue
from typing import Optional

import requests
from bs4 import BeautifulSoup


def get_sublinks(page_link: str) -> list[str]:
    response = requests.get(page_link)
    soup = BeautifulSoup(response.text, "html.parser")
    div_content = soup.find("div", class_="mw-content-ltr mw-parser-output")
    if not div_content:
        return []
    else:
        return [
            "https://en.wikipedia.org" + link.get("href")
            for link in div_content.find_all("a", href=re.compile("^/wiki/+"))
        ]


def check_link(
    queue: Queue, result_path: list[str], end_page: str, visited: DictProxy, is_found: ListProxy, unique: bool
) -> Optional[list[str]]:
    current_path = queue.get()
    current_link = current_path[-1]

    sublinks = get_sublinks(current_link)
    for sublink in sublinks:
        if sublink in visited:
            continue
        else:
            visited[sublink] = sublink
        if unique and sublink in result_path:
            continue

        if sublink == end_page:
            is_found.append(True)
            print(f"{current_process().name} found path from {current_path[0]} to {end_page}")
            return current_path + [sublink]
        else:
            queue.put(current_path + [sublink])


def multiprocess_find_path(
    result_path: list[str], start_page: str, end_page: str, process_cnt: int, unique: bool
) -> Optional[list[str]]:
    manager = Manager()
    queue: Queue = manager.Queue()
    queue.put([start_page])
    visited = manager.dict()
    is_found = manager.list([False])

    for depth in range(1, 6):
        print(f"Current depth is {depth}")
        with ProcessPoolExecutor(max_workers=process_cnt) as executor:
            futures = [
                executor.submit(check_link, queue, result_path, end_page, visited, is_found, unique)
                for _ in range(queue.qsize())
            ]

            for future in as_completed(futures):
                result = future.result()
                if result:
                    for child in active_children():
                        child.kill()
                    result_path += result[: len(result) - 1]
                    return result

    print("Not found path with depth: 5")


if __name__ == "__main__":
    pass
