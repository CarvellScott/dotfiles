#!/usr/bin/env python3
import pathlib
import re
from completion_helper import helper


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
            lines = f.readlines()
            lines = filter(lambda i: not i.startswith("!"), lines)
            lines = map(lambda i: re.match("[^\t][^\t]*\t", i).group(0), lines)
            lines = map(lambda i: i.strip(), lines)
            tags = list(set(lines))
            tags.sort()
    return tags


def completion_hook(cmd, curr_word, prev_word, **kwargs):
    matches = []
    if curr_word.startswith("-"):
        matches.append("-t")

    if prev_word == "-t":
        potential_matches = _get_tags()
        matches += [k for k in potential_matches if k.startswith(curr_word)]
    return matches


def main():
    # The easy way
    if True:
        helper(completion_hook)
    # The hard way
    else:
        results = completion_hook(*sys.argv[1:])
        if len(results):
             print("\n".join(results))


if __name__ == "__main__":
    main()
