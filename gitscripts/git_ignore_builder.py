#!/usr/bin/env python3
import argparse
import pathlib
import subprocess


def find_gitignore():
    cwd = pathlib.Path.cwd()
    git_folder = None
    for path in [cwd] + list(cwd.parents):
        git_folder = path / ".git"
        if git_folder.exists():
            break
    git_ignore_location = git_folder.parent / ".gitignore"
    print(str(git_ignore_location))
    return git_ignore_location


def read_gitignore(gitignore_path):
    lines = None
    with open(gitignore_path, "r") as f:
        lines = map(lambda _: _.strip(), f.readlines())
        lines = set(lines)
    return lines


def main():
    gitignore_path = find_gitignore()
    lines = set()
    if gitignore_path.exists():
        lines = read_gitignore(gitignore_path)
    mandatory = {
        ".*.sw?",
        "*.py[cdo]",
        "__py_cache__/"
    }
    missing = mandatory - lines
    with open(gitignore_path, "a") as f:
        for _ in sorted(missing):
            print(_, file=f)


if __name__ == "__main__":
    main()
