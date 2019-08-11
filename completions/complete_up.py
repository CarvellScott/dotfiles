#!/usr/bin/env python3
import pathlib
import os
import unittest
import shlex

try:
    import completion_utils
except (ImportError, ModuleNotFoundError):
    import df_completion_utils as completion_utils


class CompletionTestCase_up(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_path = "/mnt/c/Users/U/Userutils/foobar"
        self.exe = __file__

    @property
    def path(self):
        # Set an environment variable to contain the path and decouple the test
        # results from the current directory.
        return os.environ["COMPLETE_UP_TEST_DIRECTORY"]

    @path.setter
    def path(self, path):
        # The completion script gets called as a part of a subprocess, so you
        # can't simply pass a constant path to it. You need to set an
        # environment variable so it knows that it's testing stuff.
        os.environ["COMPLETE_UP_TEST_DIRECTORY"] = path

    def assert_completion(self, comp_line, expected):
        """
        A sort of custom assertion specifically for bash completion.
        """
        stdout = completion_utils.bash_complete(comp_line, self.exe)
        actual_list = set(stdout.splitlines())
        expected_list = set(expected)
        err = f"\nExpected: {expected_list}\nActual: {actual_list}"
        assert actual_list == expected_list, err

    def test_blank(self):
        # Exact match should show EVERYTHING
        self.path = self.test_path
        expected = {
            "/",
            "c/",
            "mnt/",
            "U/",
            "Users/",
            "Userutils/"
        }
        # assert os.environ["COMPLETE_UP_TEST_DIRECTORY"]
        self.assert_completion("up ", expected)

    def test_specifics_give_exact_path(self):
        # Exact match should give the path.
        self.path = self.test_path
        self.assert_completion("up U/", ["/mnt/c/Users/U"])

    def test_ambiguity_gives_keys(self):
        # Ambiguous match should give keys that start with the input.
        self.path = self.test_path
        expected = {
            "Users/",
            "Userutils/"
        }
        self.assert_completion("up Us", expected)

    def test_you_are_here_already(self):
        # The script shouldn't bother suggesting the current directory.
        self.path = self.test_path
        self.assert_completion("up foobar", "")


@completion_utils.bash_completion_decorator
def completion_hook(cmd, curr_word, prev_word):
    matches = []
    # This environment variable is presumed to only be set in the test case.
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

    # Return the KEY to the paths that match the arguments
    matches = {s for s in path_dict.keys() if s.startswith(cmd_args)}

    # But if it's been narrowed down, return the full path
    if len(matches) == 1:
        matches = {str(path_dict[matches.pop()])}

    return matches


if __name__ == "__main__":
    completion_hook()
