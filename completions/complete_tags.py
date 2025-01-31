#!/usr/bin/env python3
import os
import pathlib
import re
import shlex
import sys


def _get_tags():
    tags = []
    curr_path = pathlib.Path()
    tags_path = curr_path / "tags"

    # Search the current directory, then parent directories for tags file
    if not tags_path.exists():
        for parent in curr_path.absolute().parents:
            tags_path = parent / "tags"
            if tags_path.exists():
                break

    # If the tags file exists, open it and build a sorted list of tags.
    if tags_path.exists():
        with open(tags_path, "r") as f:
            regex = re.compile(r"[^\t]+\t")
            lines = f.readlines()
            lines = filter(lambda i: not i.startswith("!"), lines)
            lines = map(lambda i: regex.match(i).group(0), lines)
            lines = map(lambda i: i.strip(), lines)
            tags = lines
    return tags


def completion_hook(command, curr_word, prev_word):
    for tag in _get_tags():
        if tag.startswith(curr_word):
            yield tag


def main():
    shell = os.environ.get("SHELL")
    results = []
    if "bash" in shell:
        results = completion_hook(*sys.argv[1:])

    if "zsh" in shell:
        command = os.environ.get("COMP_LINE", "")
        command_split = shlex.split(command) + [""]
        curr_word = command_split[int(os.environ.get("COMP_CWORD", 0))]
        results = completion_hook(command, curr_word, None)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
