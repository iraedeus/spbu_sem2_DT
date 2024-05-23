import pytest

from src.exam.exam_3.path_finder import multiprocess_path_finder


@pytest.mark.parametrize(
    "path",
    [
        [
            "https://en.wikipedia.org/wiki/Court-martial",
            "https://en.wikipedia.org/wiki/Drumhead_court-martial",
            "https://en.wikipedia.org/wiki/Adolf_Hitler",
        ]
    ],
)
def test_multiprocess_path_finder(path):
    assert multiprocess_path_finder(3, 14, path[0]) == path


def test_no_path():
    assert multiprocess_path_finder(2, 14, "https://en.wikipedia.org/wiki/Court-martial") == ["", "", ""]
