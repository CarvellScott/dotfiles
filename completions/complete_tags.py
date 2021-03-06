#!/usr/bin/env python3
import pathlib
import re
import sys

try:
    import completion_utils
except (ImportError, ModuleNotFoundError):
    import df_completion_utils as completion_utils


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
            lines = map(lambda i: re.match(r"[^\t]+\t", i).group(0), lines)
            lines = map(lambda i: i.strip(), lines)
            tags = list(set(lines))
            tags.sort()
    return tags


class CompleteTags(completion_utils.BashCompletion):
    def completion_hook(self, cmd, curr_word, prev_word):
        matches = [k for k in _get_tags() if k.startswith(curr_word)]
        return matches

if __name__ == "__main__":
    CompleteTags().main()
