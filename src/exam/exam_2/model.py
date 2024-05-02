import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
from numpy.compat import unicode


def parse_quotes(page) -> list[str]:
    soup = BeautifulSoup(page.text, "html.parser")
    quote_list = soup.findAll("div", class_="quote__body")
    quotes_text = []
    for i in range(1, 11):
        str = ""
        for child in quote_list[i].children:
            if unicode(child) != "<br/>":
                str += child.strip() + "\n"
        quotes_text.append(str)

    return list(reversed(quotes_text))


async def get_new():
    page = requests.get("https://башорг.рф/")
    await asyncio.sleep(5)
    return [quote for quote in parse_quotes(page)]



async def get_best():
    page = requests.get("https://башорг.рф/best/2024")
    await asyncio.sleep(2)
    return [quote for quote in parse_quotes(page)]


async def get_random():
    page = requests.get("https://башорг.рф/random")
    return [quote for quote in parse_quotes(page)]

print(asyncio.run(get_best()))