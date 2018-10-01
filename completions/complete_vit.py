#!/usr/bin/env python3
import re
from completion_helper import helper


def _get_tags():
    lines = []
    with open("./tags") as f:
        lines = f.readlines()
    lines = filter(lambda i: not i.startswith("!"), lines)
    lines = map(lambda i: re.match("[^\t][^\t]*\t", i).group(0), lines)
    lines = map(lambda i: i.strip(), lines)
    return list(set(lines))


def completion_hook(cmd, curr_word, prev_word, **kwargs):
    potential_matches = _get_tags()
    matches = [k for k in potential_matches if k.startswith(curr_word)]
    return matches


def main():
    # The hard way
    # results = completion_hook(*sys.argv[1:])
    # if len(results):
    #     print("\n".join(results))
    helper(completion_hook)


if __name__ == "__main__":
    main()
