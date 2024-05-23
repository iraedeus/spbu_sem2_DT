import copy
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from queue import Queue
from typing import Optional

import requests
from bs4 import BeautifulSoup


def get_name_of_page() -> str:
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("span", "mw-page-title-main").text


def get_sublinks(page_link: str) -> list[str]:
    response = requests.get(page_link)
    soup = BeautifulSoup(response.text, "html.parser")
    div_content = soup.find("div", class_="mw-content-ltr mw-parser-output")
    if div_content:
        all_links = [
            "https://en.wikipedia.org" + link.get("href")
            for link in div_content.find_all("a", href=re.compile("^/wiki/+"))
        ]
        good_links = []
        for link in all_links:
            name_of_page = link.split("/wiki/")[-1]
            if ":" not in name_of_page and "ISBN" not in name_of_page:
                good_links.append(link)

        return good_links
    else:
        return []


def path_finder(depth: int, init_page_link: str, sub_links: list[str]) -> Optional[list[str]]:
    queue: Queue = Queue(-1)
    for sub_link in sub_links:
        queue.put([init_page_link, sub_link])
    depth = 0
    while queue.qsize() != 0:
        current_path = queue.get()
        if len(current_path) - 1 == depth:
            break
        if len(current_path) - 1 > depth:
            depth = len(current_path)

        last_url = current_path[-1]
        next_links = get_sublinks(last_url)

        for link in next_links:
            if link == "https://en.wikipedia.org/wiki/Adolf_Hitler":
                print()
                return current_path + [link]
            else:
                queue.put(current_path + [link])

    return None


def multiprocess_path_finder(depth: int, multiprocess_count: int, init_page_link: str) -> list[str]:
    sublinks = get_sublinks(init_page_link)

    if len(sublinks) < multiprocess_count:
        size = 1
    else:
        size = len(sublinks) // multiprocess_count
    sub_links = [sublinks[i : i + size] for i in range(0, len(sublinks), size)]

    with ProcessPoolExecutor(max_workers=multiprocess_count) as executor:
        paths = [executor.submit(path_finder, depth, init_page_link, sub_link) for sub_link in sub_links]
        minimal_path = [""] * (depth + 1)
        for path in as_completed(paths):
            result = path.result()
            if not result:
                continue
            if len(result) < len(minimal_path):
                minimal_path = result
        return minimal_path


if __name__ == "__main__":
    pass
