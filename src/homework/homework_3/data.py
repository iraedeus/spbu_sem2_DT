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
