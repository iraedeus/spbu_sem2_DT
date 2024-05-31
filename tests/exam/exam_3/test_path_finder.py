import pytest

from src.exam.exam_3.main import get_path_between_two
from src.exam.exam_3.path_finder import multiprocess_find_path


@pytest.mark.parametrize(
    "first_link, second_link ,expected",
    [
        (
            "Blood_(video_game)",
            "Adolf_Hitler",
            [
                "https://en.wikipedia.org/wiki/Blood_(video_game)",
                "https://en.wikipedia.org/wiki/Europe",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        ),
        (
            "Skibidi_Toilet",
            "Adolf_Hitler",
            [
                "https://en.wikipedia.org/wiki/Skibidi_Toilet",
                "https://en.wikipedia.org/wiki/Parody",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        ),
    ],
)
def test_get_between(first_link, second_link, expected):
    assert get_path_between_two([], first_link, second_link, 10, False) == expected


@pytest.mark.parametrize(
    "links, expected",
    [
        (
            ["Skibidi_Toilet", "Russia", "Adolf_Hitler"],
            [
                "https://en.wikipedia.org/wiki/Skibidi_Toilet",
                "https://en.wikipedia.org/wiki/Georgia_(country)",
                "https://en.wikipedia.org/wiki/Russia",
                "https://en.wikipedia.org/wiki/Authoritarianism",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        ),
        (
            ["Twitch_(service)", "PewDiePie", "Vietnam_War", "Adolf_Hitler"],
            [
                "https://en.wikipedia.org/wiki/Twitch_(service)",
                "https://en.wikipedia.org/wiki/Cr1TiKaL",
                "https://en.wikipedia.org/wiki/PewDiePie",
                "https://en.wikipedia.org/wiki/Satire",
                "https://en.wikipedia.org/wiki/Vietnam_War",
                "https://en.wikipedia.org/wiki/Cold_War",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        ),
    ],
)
def get_multiple(links, expected):
    output = []
    for i in range(len(links) - 1):
        multiprocess_find_path(output, links[i], links[i + 1], 10, False)

    assert output + links[: len(links) - 1] == expected
