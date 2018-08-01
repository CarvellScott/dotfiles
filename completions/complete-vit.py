#!/usr/bin/env python3.5
import os
import re
import sys


def get_tags():
    lines = []
    with open("./tags") as f:
        lines = f.readlines()
    lines = filter(lambda i: not i.startswith("!"), lines)
    lines = map(lambda i: re.match("[^\t][^\t]*\t", i).group(0), lines)
    lines = map(lambda i: i.strip(), lines)
    return list(set(lines))


def completion_hook(command, current_word, previous_word):
    potential_matches = get_tags()
    matches = [k for k in potential_matches if k.startswith(current_word)]
    return matches


def main():
    results = completion_hook(*sys.argv[1:])
    if len(results):
        print("\n".join(results))


if __name__ == "__main__":
    main()
