#!/usr/bin/env python3
import pathlib
from completion_helper import helper


def completion_hook(cmd, curr_word, prev_word, **kwargs):
    matches = []
    curr_path = pathlib.Path().absolute()
    paths = list(curr_path.parents)

    if "/" in prev_word:
        return matches

    # This allows path completion as normal
    if "/" in curr_word and len(curr_word) > 0:
        return [str(p) for p in paths if str(p).startswith(curr_word)]

    # Map path parts to parent paths, prioritizing those in proximity.
    path_dict = {}
    for p in reversed(paths):
        # p.stem returns "" for a path of "/", so we use p.parts[-1] instead
        path_dict[p.parts[-1]] = p

    # Return the path if there's an exact match in path_dict
    # Even if there's a word that starts with curr_word, the shortest takes
    # priority.
    if curr_word in path_dict.keys():
        matches = [str(path_dict[curr_word])]
    else:
        # If no exact match, do a fuzzy match for part of the path
        matches = [s for s in path_dict.keys() if s.startswith(curr_word)]
        # Return the path if it's been narrowed down.
        if len(matches) == 1:
            matches = [str(path_dict[matches[0]])]

    return matches


def main():
    helper(completion_hook)


if __name__ == "__main__":
    main()
