#!/usr/bin/env python3
import pathlib
import re
from completion_utils import bash_completion_decorator


def _get_tags():
    tags = []
    curr_path = pathlib.Path()
    tags_path = curr_path / "tags"

    # Search the current directory, then parent directories for tags file
    if False:
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
            lines = map(lambda i: re.match(r"[^\t]+\t", i).group(0), lines)
            lines = map(lambda i: i.strip(), lines)
            tags = list(set(lines))
            tags.sort()
    return tags


@bash_completion_decorator
def completion_hook(cmd, curr_word, prev_word):
    matches = []
    if curr_word.startswith("-"):
        matches.append("-t")

    if prev_word == "-t":
        potential_matches = _get_tags()
        matches += [k for k in potential_matches if k.startswith(curr_word)]
    return matches


if __name__ == "__main__":
    completion_hook()
