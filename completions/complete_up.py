#!/usr/bin/env python3
import pathlib
import re
import sys


def completion_hook(command, curr_word, prev_word):
    matches = []
    try:
        curr_path = pathlib.Path().absolute()
    except FileNotFoundError:
        curr_path = pathlib.Path.home().absolute()

    paths = list(curr_path.parents)
    if curr_path == pathlib.Path.home():
        paths += [curr_path]

    # Greedy regexes will match the path closest to curr_path
    paths = map(str, paths)
    regex = re.compile(r".*{}".format(re.escape(curr_word)))
    matches = {s for s in paths if regex.search(s)}
    return matches

def main():
    results = completion_hook(*sys.argv[1:])
    if len(results):
        print("\n".join(results))


if __name__ == "__main__":
    main()
