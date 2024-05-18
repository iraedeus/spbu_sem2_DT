import argparse
from base64 import b64decode
from typing import Any

import requests

from src.homework.homework_3.data import Branch, Commit, Owner, PullRequest, ReadmeFile, Repo

USER_CHOICES = (
    "1) Get general info about repo \n"
    "2) Get pull request info \n"
    "3) Get history of commit from branch \n"
    "4) Exit\n"
)


def parse_args() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str)
    parser.add_argument("repo_name", type=str)
    args = parser.parse_args()
    output: tuple[str, str] = (args.username, args.repo_name)

    return output


def get_repo(username: str, repo_name: str) -> dict[str, Any]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
    return repo_response.json()


def get_readme(username: str, repo_name: str) -> dict[str, Any]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/contents/README.md")
    return repo_response.json()


def get_pull_requests(username: str, repo_name: str) -> list[dict[str, Any]]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/pulls")
    return repo_response.json()


def get_branches(username: str, repo_name: str) -> list[dict[str, Any]]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/branches")
    return repo_response.json()


def output_owner(owner: Owner) -> str:
    output_str = f"--Owner username: {owner.login}, id: {owner.id}.\n" f"--Url to profile: {owner.html_url}"
    return output_str


def output_repo_info(repo: Repo, readme: ReadmeFile) -> None:
    def output_readme(readme: ReadmeFile) -> str:
        if readme.name:
            readme_data = b64decode(readme.content).decode()
            output_str = f"File name: {readme.name}\n" f"{str(readme_data)}"
            return output_str
        else:
            return "Not found"

    owner_info = output_owner(repo.owner)
    readme_info = output_readme(readme)
    print(
        f"Repo name: {repo.name} \n"
        f"Repo id: {repo.id}\n"
        f"{owner_info}\n"
        f"Language: {repo.language}\n\n"
        f"Info about repo from README.txt: \n"
        f"{readme_info}\n"
    )


def output_pull_info(pull: PullRequest) -> None:
    def output_rewievers(requested_reviewers: list[Owner]) -> str:
        str = ""
        for reviewer in requested_reviewers:
            output_str = (
                f"--Reviewer username: {reviewer.login}, id: {reviewer.id}.\n" f"--Url to profile: {reviewer.html_url}"
            )
            str += output_str + "\n"
            str += "\n"
        return str.rstrip("\n")

    owner_info = output_owner(pull.user)
    reviewers_info = output_rewievers(pull.requested_reviewers)
    print(
        f"Pull name: {pull.title} \n"
        f"id: {pull.id}\n"
        f"{owner_info}\n"
        f"Reviewers: \n"
        f"{reviewers_info}\n"
        f"Pull branch: {pull.head.ref}\n"
        f"Merging into: {pull.base.ref}\n"
    )


def output_pulls(pulls: list[PullRequest]) -> None:
    pull_number = 1
    for pull in pulls:
        print(f"{pull_number}) Pull name: {pull.title}")
        pull_number += 1

    user_choice = input("Choose a pull's number: ")
    try:
        pull_number = int(user_choice) - 1
        output_pull_info(pulls[pull_number])
    except:
        print("Incorrect number of pull request\n")


def output_commits(branch: Branch) -> None:
    last_commit_url = branch.commit.url

    def get_commit_from_url(url: str) -> dict[str, Any]:
        response = requests.get(url)
        return response.json()

    def recursion(current_commit: Commit) -> None:
        if current_commit.parents == []:
            return None
        parent = current_commit.parents[0]
        parent_commit = Commit.from_dict(get_commit_from_url(parent.url))
        messages = current_commit.commit.message.split("\n")
        recursion(parent_commit)
        str = ""
        for message in messages:
            str += f"|     {message}\n"

        print(
            f"commit: {current_commit.sha} \n"
            f"|    \n"
            f"|    \n"
            f"{str}"
            f"|    \n"
            f"|    \n"
            f"------------------------------"
        )

    json_dict = get_commit_from_url(last_commit_url)
    last_commit_obj = Commit.from_dict(json_dict)
    recursion(last_commit_obj)


def output_branches(branches: list[Branch]) -> None:
    branch_number = 1
    for branch in branches:
        print(f"{branch_number}) Branch name: {branch.name}")
        branch_number += 1

    user_choice = input("Choose a branch number: ")
    try:
        branch_number = int(user_choice) - 1
        output_commits(branches[branch_number])
    except Exception as error:
        print(error)
        print("Incorrect number of branch\n")


def main() -> None:
    args = parse_args()
    repo = None
    readme = None
    pulls = None
    branches = None

    while True:
        user_choice = input(USER_CHOICES)

        if user_choice == "1":
            repo = Repo.from_dict(get_repo(*args))
            readme = ReadmeFile.from_dict(get_readme(*args))
            output_repo_info(repo, readme)

        elif user_choice == "2":
            pulls = [PullRequest.from_dict(asdict_obj) for asdict_obj in get_pull_requests(*args)]
            if len(pulls) != 0:
                output_pulls(pulls)
            else:
                print("Can't find any pull requests")

        elif user_choice == "3":
            branches = [Branch.from_dict(asdict_obj) for asdict_obj in get_branches(*args)]
            output_branches(branches)

        elif user_choice == "4":
            break
        else:
            print("You chosen incorrect action")


if __name__ == "__main__":
    main()
