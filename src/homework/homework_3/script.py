import argparse
import json
from base64 import b64decode

import requests
from data import Owner, PullRequest, ReadmeFile, Repo
from json_parser import parse_json

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


def write_info_repo(username: str, repo_name: str) -> None:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
    str_json = json.dumps(repo_response.json())
    with open("repo.json", "w+") as file:
        file.write(str_json)


def write_readme(username: str, repo_name: str) -> None:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/contents/README.md")
    str_json = json.dumps(repo_response.json())
    with open("readme.json", "w+") as file:
        file.write(str_json)


def output_owner(owner: Owner) -> str:
    output_str = f"--Owner username: {owner.login}, id: {owner.id}.\n" f"--Url to profile: {owner.html_url}"
    return output_str


def output_to_user_first_choice(repo: Repo, readme: ReadmeFile) -> None:
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


def write_pull_requests(username: str, repo_name: str) -> None:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/pulls")
    str_json = json.dumps(repo_response.json())
    with open("pulls.json", "w+") as file:
        file.write(str_json)


def output_pull(pull: PullRequest) -> None:
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


def pulls_choice(pulls: list[PullRequest]) -> None:
    print("Choose a pull's number")
    pull_number = 1
    for pull in pulls:
        print(f"{pull_number}) Pull name: {pull.title}")
        pull_number += 1

    user_choice = input()
    try:
        pull_number = int(user_choice) - 1
        output_pull(pulls[pull_number])
    except Exception as err:
        print(err)
        print("Incorrect number of pull request\n")


def get_all_json(args: tuple[str, str]) -> None:
    write_info_repo(*args)
    write_readme(*args)
    write_pull_requests(*args)


def main() -> None:
    args = parse_args()
    get_all_json(args)
    repo = Repo.from_dict(parse_json("repo.json"))
    readme = ReadmeFile.from_dict(parse_json("readme.json"))
    pulls = [PullRequest.from_dict(asdict_obj) for asdict_obj in parse_json("pulls.json")]
    while True:
        user_choice = input(USER_CHOICES)
        if user_choice == "1":
            output_to_user_first_choice(repo, readme)
        elif user_choice == "2":
            pulls_choice(pulls)
        elif user_choice == "3":
            pass
        elif user_choice == "4":
            break
        else:
            print("You chosen incorrect action")


if __name__ == "__main__":
    main()
