#!/usr/bin/env python3
import pathlib
import os
import unittest
import shlex
from completion_helper import bash_complete, bash_completion_decorator


class CompletionTestCase_up(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exe = __file__
        self.path = "/mnt/c/Users/U/Userutils/foobar"

    @property
    def path(self):
        # Set an environment variable to contain the path and decouple the test
        # results from the current directory.
        return os.environ["COMPLETE_UP_TEST_DIRECTORY"]

    @path.setter
    def path(self, path):
        os.environ["COMPLETE_UP_TEST_DIRECTORY"] = path

    def assert_completion(self, comp_line, expected):
        """
        A sort of custom assertion specifically for bash completion.
        """
        with self.subTest(comp_line=comp_line, path=self.path):
            stdout = bash_complete(comp_line, self.exe)
            actual_list = repr(sorted(stdout.splitlines()))
            expected_list = repr(sorted(expected.splitlines()))
            err = f"\nExpected: {expected_list}\nActual: {actual_list}"
            assert actual_list == expected_list, err

    def test_blank(self):
        # Exact match should show EVERYTHING
        self.assert_completion("up ", "/\nc/\nmnt/\nU/\nUsers/\nUserutils/")

    def test_specifics_give_exact_path(self):
        # Exact match should give the path.
        self.assert_completion("up U/", "/mnt/c/Users/U")

    def test_ambiguity_gives_keys(self):
        # Ambiguous match should give keys that start with the input.
        self.assert_completion("up Us", "Users/\nUserutils/")

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

    comp_line = os.environ["COMP_LINE"]
    cmd_args = comp_line[len(cmd) + 1:]

    # Map path parts to parent paths, prioritizing things closer to the end as
    # keys.
    path_dict = {}
    for p in reversed(paths):
        # p.stem returns "" for a path of "/", so we use p.parts[-1] instead
        key = p.parts[-1]
        if not key.endswith("/"):
            key += "/"
        key = shlex.quote(key) if " " in key else key
        path_dict[key] = p

    matches = [s for s in path_dict.keys() if s.startswith(cmd_args)]

    # Return the path if it's been narrowed down.
    if len(matches) == 1:
        matches = [str(path_dict[matches[0]])]

    return matches


if __name__ == "__main__":
    completion_hook()
