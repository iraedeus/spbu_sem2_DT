from io import StringIO

import pytest

from src.homework.homework_3 import script
from src.homework.homework_3.script import *


@pytest.mark.parametrize(
    "username, repo_name, expected_username, expected_repo_name",
    [
        ("iraedeus", "spbu_sem2_DT", "iraedeus", "spbu_sem2_DT"),
        ("iraedeus", "spbu_sem1_DT", "iraedeus", "spbu_sem1_DT"),
        ("xImoZA", "python_spbu_TP23_sem2", "xImoZA", "python_spbu_TP23_sem2"),
    ],
)
def test_get_repo(username, repo_name, expected_repo_name, expected_username):
    repo_dict = get_repo(username, repo_name)
    assert repo_dict["owner"]["login"] == expected_username
    assert repo_dict["name"] == expected_repo_name


@pytest.mark.parametrize(
    "username, repo_name, expected",
    [
        (
            "iraedeus",
            "spbu_sem2_DT",
            "IyBzYnB1X3NlbTIKUHJhY3RpY2llcyBhbmQgaG9tZXdvcmtzIG9mIDIgc2Vt\nZXN0ZXIgU1BiVQo=\n",
        ),
        ("iraedeus", "spbu_sem1_DT", "IyBzcGJ1X3NlbTFfRFQKUmVwb3NpdG9yeSBmb3IgcHJhY3RpY2VzIGFuZCBo\nb21ld29ya3MK\n"),
        (
            "xImoZA",
            "python_spbu_TP23_sem2",
            "IyBweXRob25fc3BidV9UUDIzX3NlbTIKUHJhY3RpY2VzIGFuZCBob21ld29y\nayBzcGJ1IHNlbWVzdGVyIDIK\n",
        ),
    ],
)
def test_get_readme(username, repo_name, expected):
    readme_dict = get_readme(username, repo_name)
    assert readme_dict["content"] == expected


@pytest.mark.parametrize(
    "username, repo_name, expected",
    [
        (
            "iraedeus",
            "spbu_sem1_DT",
            [
                "Homework 6 Task 2.Totjmyanin",
            ],
        ),
        ("iraedeus", "test", []),
    ],
)
def test_get_pull_requests(username, repo_name, expected):
    pulls = get_pull_requests(username, repo_name)
    name_of_pulls = [pull["title"] for pull in pulls]
    assert set(name_of_pulls) == set(expected)


@pytest.mark.parametrize(
    "username, repo_name, expected",
    [
        ("iraedeus", "spbu_sem1_DT", ["main", "homework-6-1", "homework-13", "test-2-2", "test_3_1", "homework-6-2"]),
        ("iraedeus", "test", ["main", "c", "test"]),
    ],
)
def test_get_branches(username, repo_name, expected):
    branches = get_branches(username, repo_name)
    branches_names = [branch["name"] for branch in branches]
    assert set(branches_names) == set(expected)


@pytest.mark.parametrize(
    "username, repo_name, actions, expected",
    [
        (
            "iraedeus",
            "spbu_sem1_DT",
            ["1", "4"],
            "Repo name: spbu_sem1_DT \n"
            "Repo id: 691124303\n"
            "--Owner username: iraedeus, id: 144918156.\n"
            "--Url to profile: https://github.com/iraedeus\n"
            "Language: Python\n"
            "\n"
            "Info about repo from README.txt: \n"
            "File name: README.md\n"
            "# spbu_sem1_DT\n"
            "Repository for practices and homeworks\n"
            "\n\n",
        ),
        ("iraedeus", "test", ["2", "4"], "Can't find any pull requests\n"),
        (
            "iraedeus",
            "spbu_sem1_DT",
            ["2", "1", "4"],
            "1) Pull name: Homework 6 Task 2.Totjmyanin\n"
            "Pull name: Homework 6 Task 2.Totjmyanin \n"
            "id: 1614901155\n"
            "--Owner username: iraedeus, id: 144918156.\n"
            "--Url to profile: https://github.com/iraedeus\n"
            "Reviewers: \n\n"
            "Pull branch: homework-6-2\n"
            "Merging into: homework-6-1\n\n",
        ),
        (
            "iraedeus",
            "test",
            ["3", "1", "4"],
            "1) Branch name: c\n"
            "2) Branch name: main\n"
            "3) Branch name: test\n"
            "commit: 43282ae13aa17017e9553333e1de2d8773183452 \n"
            "|    \n"
            "|    \n"
            "|     gg\n"
            "|    \n"
            "|    \n"
            "------------------------------\n"
            "commit: 9db79f0a859deaf3500099c1db9f8d7b3819e9e3 \n"
            "|    \n"
            "|    \n"
            "|     qqq\n"
            "|    \n"
            "|    \n"
            "------------------------------\n"
            "commit: fae4a5cad5f951cf05d86c03c2cf6e54feeda4cc \n"
            "|    \n"
            "|    \n"
            "|     Init\n"
            "|    \n"
            "|    \n"
            "------------------------------\n"
            "commit: ae44908666a488b46cf9af97337d89370382070f \n"
            "|    \n"
            "|    \n"
            "|     Merge branches 'a' and 'b' into c\n"
            "|    \n"
            "|    \n"
            "------------------------------\n"
            "commit: 2942fd4ac2e8d23c5df6ea07063128414d430472 \n"
            "|    \n"
            "|    \n"
            "|     2\n"
            "|    \n"
            "|    \n"
            "------------------------------\n"
            "commit: 4f2136f4da9ecfc1fa6492a62696850b087882f1 \n"
            "|    \n"
            "|    \n"
            "|     Merge branches 'a' and 'b' into c\n"
            "|    \n"
            "|    \n"
            "------------------------------\n",
        ),
    ],
)
def test_main_scenario(username, repo_name, actions, expected, monkeypatch):
    def mock_parse_args():
        return username, repo_name

    monkeypatch.setattr(script, "parse_args", mock_parse_args)
    monkeypatch.setattr("builtins.input", lambda _: actions.pop(0))
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    value = fake_output.getvalue()
    assert value == expected
