import requests
from bs4 import BeautifulSoup
from numpy.compat import unicode
from requests import Response


def parse_quotes(page: Response, quote_count: int) -> list[str]:
    soup = BeautifulSoup(page.text, "html.parser")
    quote_list = soup.findAll("div", class_="quote__body")
    quotes_text = []
    for i in range(1, quote_count + 1):
        str = f"{i} цитата: \n"
        for child in quote_list[i].children:
            if unicode(child) != "<br/>" and child.text.strip() != "Комикс по мотивам цитаты":
                if len(child) > 0:
                    str += child.strip() + "\n"
        quotes_text.append(str)

    return list(reversed(quotes_text))


async def get_new(quote_count: int = 10) -> list[str]:
    page = requests.get("https://башорг.рф/")
    return [quote for quote in parse_quotes(page, quote_count)]


async def get_best(quote_count: int = 10) -> list[str]:
    page = requests.get("https://башорг.рф/best/2024")
    return [quote for quote in parse_quotes(page, quote_count)]


async def get_random(quote_count: int = 10) -> list[str]:
    page = requests.get("https://башорг.рф/random")
    return [quote for quote in parse_quotes(page, quote_count)]


if __name__ == "__main__":
    pass
