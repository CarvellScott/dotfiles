#!/usr/bin/env python3
import pathlib
import os
import unittest
from completion_helper import bash_complete, bash_completion_decorator


class CompletionTestCase_up(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exe = __file__
        path = "/mnt/c/Users/U/Userutils/foobar"
        # Set an environment variable to contain the path and decouple the test
        # results from the current directory.
        os.environ["COMPLETE_UP_TEST_DIRECTORY"] = path

    def assert_completion(self, comp_line, expected):
        """
        A sort of custom assertion specifically for bash completion.
        """
        stdout = bash_complete(comp_line, self.exe)
        self.assertEqual(stdout, expected)

    def test_perfect_match_max_priority(self):
        # Exact match should give the path.
        self.assert_completion("up U", "/mnt/c/Users/U")

    def test_ambiguity_gives_keys(self):
        # Ambiguous match should give keys that start with the input.
        self.assert_completion("up Us", "Users\nUserutils")

    def test_you_are_here_already(self):
        # The script shouldn't bother suggesting the current directory.
        self.assert_completion("up foobar", "")


@bash_completion_decorator
def completion_hook(cmd, curr_word, prev_word):
    matches = []
    # If you set this evironment variable, outside of the test case above that
    # does so, you deserve whatever happens to you.
    test_path = os.environ.get("COMPLETE_UP_TEST_DIRECTORY")
    curr_path = None
    if test_path:
        curr_path = pathlib.Path(test_path)
    else:
        curr_path = pathlib.Path().absolute()

    paths = list(curr_path.parents)

    if "/" in prev_word:
        return matches

    # This allows path completion as normal
    if "/" in curr_word and len(curr_word) > 0:
        return [str(p) for p in paths if str(p).startswith(curr_word)]

    # Map path parts to parent paths, prioritizing things closer to the end as
    # keys.
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


if __name__ == "__main__":
    completion_hook()
