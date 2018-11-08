#!/usr/bin/env python3
import pathlib
import re
from completion_helper import helper


def _get_tags():
    curr_path = pathlib.Path()


def completion_hook(cmd, curr_word, prev_word, **kwargs):
    matches = []
    curr_path = pathlib.Path().absolute()
    paths = list(curr_path.parents)

    if "/" in prev_word:
        return matches

    stems = curr_path.parts
    path_dict = {}
    for p in reversed(paths):
        path_dict[p.stem] = p
    if curr_word:
        # First complete a word that makes up a part of the path
        if curr_word not in stems:
            matches = [s for s in stems if s.startswith(curr_word)]
            if len(matches) == 1:
                matches = [str(path_dict[s]) for s in matches]
            else:
                matches = [str(p) for p in paths if str(p).endswith(curr_word)]
        if curr_word in path_dict.keys():
            matches = [path_dict[curr_word]]
    else:
        matches = list(stems)
        #return [k + ":" + str(v) for k, v in path_dict.items() if str(k).startswith(curr_word)]
        #return [str(p) for p in paths if str(p).startswith(curr_word)]

    # Note the instances where I return the stems instead of the full paths.
    return matches


def main():
    helper(completion_hook)

if __name__ == "__main__":
    main()
