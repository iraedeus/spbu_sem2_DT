from dataclasses import dataclass
from typing import Optional

from orm import ORM


@dataclass
class Owner(ORM):
    login: Optional[str] = None
    id: Optional[int] = None
    html_url: Optional[str] = None


@dataclass
class ReadmeFile(ORM):
    name: Optional[str] = None
    content: Optional[str] = None


@dataclass
class Repo(ORM):
    id: Optional[int] = None
    name: Optional[str] = None
    owner: Owner = None  # type: ignore
    language: Optional[str] = None


@dataclass
class PullRequest(ORM):
    @dataclass
    class MergingBranch(ORM):
        ref: Optional[str] = None

    title: Optional[str] = None
    id: Optional[int] = None
    user: Owner = None  # type: ignore
    requested_reviewers: list[Owner] = None  # type: ignore
    head: MergingBranch = None  # type: ignore
    base: MergingBranch = None  # type: ignore


@dataclass
class Commit(ORM):
    @dataclass
    class CommitMessage(ORM):
        message: Optional[str] = None
    @dataclass
    class Parent(ORM):
        url: Optional[str] = None

    sha: Optional[str] = None
    commit: CommitMessage = None # type: ignore
    parents: list[Parent] = None # type: ignore


@dataclass
class Branch(ORM):
    @dataclass
    class LastCommit(ORM):
        sha: Optional[str] = None
        url: Optional[str] = None

    name: Optional[str] = None
    commit: LastCommit = None  # type: ignore
