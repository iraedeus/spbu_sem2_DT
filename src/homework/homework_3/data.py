from dataclasses import dataclass

from src.homework.homework_3.orm import ORM


@dataclass
class Owner(ORM):
    login: str
    id: int
    html_url: str


@dataclass
class ReadmeFile(ORM):
    name: str
    content: str


@dataclass
class Repo(ORM):
    id: int
    name: str
    owner: Owner
    language: str


@dataclass
class PullRequest(ORM):
    @dataclass
    class MergingBranch(ORM):
        ref: str

    title: str
    id: int
    user: Owner
    requested_reviewers: list[Owner]
    head: MergingBranch
    base: MergingBranch


@dataclass
class Commit(ORM):
    @dataclass
    class CommitMessage(ORM):
        message: str

    @dataclass
    class Parent(ORM):
        url: str

    sha: str
    commit: CommitMessage
    parents: list[Parent]


@dataclass
class Branch(ORM):
    @dataclass
    class LastCommit(ORM):
        sha: str
        url: str

    name: str
    commit: LastCommit
