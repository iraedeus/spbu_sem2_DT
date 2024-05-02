import asyncio

import pytest

from src.exam.exam_2.model import *


@pytest.mark.parametrize("quote_count", [(15), (20), (5)])
def test_get_new(quote_count):
    quotes = asyncio.run(get_new(quote_count))
    assert len(quotes) == quote_count


@pytest.mark.parametrize("quote_count", [(15), (20), (5)])
def test_get_best(quote_count):
    quotes = asyncio.run(get_best(quote_count))
    assert len(quotes) == quote_count


@pytest.mark.parametrize("quote_count", [(15), (20), (5)])
def test_get_random(quote_count):
    quotes = asyncio.run(get_random(quote_count))
    assert len(quotes) == quote_count
