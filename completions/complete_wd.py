#!/usr/bin/env python3
import pathlib
import os
import unittest
import subprocess

try:
    import completion_utils
except (ImportError, ModuleNotFoundError):
    import df_completion_utils as completion_utils

# The following was generated from this command:
# lsof -a -d cwd -F -c bash | grep --color=None '^n'
# lsof normally generates a lot more, but I wanted something more brief.
sample_lsof_out = """
n/mnt/c/Users/Carvell
n/home/cscott
n/home/cscott
n/home/cscott/dotfiles/completions
n/home/cscott/dotfiles/completions
"""

TEST_DATA_KEY = "COMPLETE_WD_TEST_DATA"


def get_wd_test_data():
    return os.environ.get(TEST_DATA_KEY)


def set_wd_test_data(data):
    os.environ[TEST_DATA_KEY] = data


class CompletionTestCaseWarpDir(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exe = __file__

    def setUp(self):
        set_wd_test_data(sample_lsof_out)
        if not get_wd_test_data():
            raise Exception("No test data loaded")

    def test_happy(self):
        comp_line = "wd "
        expected = {
            "/mnt/c/Users/Carvell",
            "/home/cscott/dotfiles/completions"
        }
        stdout = completion_utils.bash_complete(comp_line, self.exe)
        actual = set(stdout.splitlines())
        home = str(pathlib.Path.home())
        cwd = str(pathlib.Path.cwd().absolute())
        expected -= {home, cwd}

        # It's okay to have other paths show up alongside the expected ones.
        err = f"\nExpected: {expected}\nActual: {actual}"
        assert expected.intersection(actual) == expected, err


@completion_utils.bash_completion_decorator
def completion_hook(cmd, curr_word, prev_word):
    matches = []
    # If you set this environment variable, outside of the test case above that
    # does so, you deserve whatever happens to you.

    line = None
    if TEST_DATA_KEY in os.environ:
        lines = get_wd_test_data().strip().splitlines()
    else:
        # To get a list of the working directory for every terminal you have
        # open, this is the closest you can get
        finished_process = subprocess.run(
            ["/usr/bin/lsof", "-a", "-d", "cwd", "-F", "-c", "bash"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        lines = finished_process.stdout.strip().splitlines()

    # All directories from the lsof command come prepended with "n".
    # Isolate the directories and put them into a set.
    paths = {_[1:] for _ in lines if _.startswith("n")}

    # Remove home and current directory. You're either already there or
    # they're easy to cd to.
    home = str(pathlib.Path.home())
    cwd = str(pathlib.Path.cwd().absolute())
    paths -= {home, cwd}

    # Finally, match against the line we were given.
    comp_line = os.environ["COMP_LINE"]
    cmd_args = comp_line[len(cmd) + 1:]
    matches = {_ for _ in paths if _.startswith(cmd_args)}

    # Return the path if it's been narrowed down.
    return matches


if __name__ == "__main__":
    completion_hook()
