#!/usr/bin/env python3
import pathlib
from completion_helper import helper


def completion_hook(cmd, curr_word, prev_word, **kwargs):
    matches = []
    curr_path = pathlib.Path().absolute()
    paths = list(curr_path.parents)

    if "/" in prev_word:
        return matches

    parts = curr_path.parts[:-1]
    # Map path parts to parent paths, prioritizing those in proximity.
    path_dict = {}
    for p in reversed(paths):
        path_dict[p.stem] = p

    if curr_word:
        # First complete a word that makes up a part of the path
        if curr_word not in parts:
            matches = [s for s in parts if s.startswith(curr_word)]
            # Return the path if we've narrowed it down.
            if len(matches) == 1:
                matches = [str(path_dict[s]) for s in matches]
        # Return the path if there's an exact match in path_dict
        # Even if there's a word that starts with curr_word, the shortest takes
        # priority.
        if curr_word in path_dict.keys():
            matches = [str(path_dict[curr_word])]
    else:
        matches = list(parts)

    return matches


def main():
    helper(completion_hook)


if __name__ == "__main__":
    main()
