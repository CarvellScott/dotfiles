#!/usr/bin/env python3
import unittest
import shlex
from completion_helper import helper, run_bash_completion


class CompletionTestCase_xclip(unittest.TestCase):
    def test_end_with_space(self):
        comp_line = "xclip -o -selection "
        stdout = run_bash_completion(comp_line, __file__)
        sorted_stdout = "\n".join(sorted(shlex.split(stdout)))
        expected = "buffer-cut\nclipboard\nprimary\nsecondary"
        self.assertEqual(sorted_stdout, expected, "\"{}\"".format(comp_line))

    def test_still_completing(self):
        # The word is still being completed, if there's another word that
        # starts with it, then that would be a viable completion option.
        comp_line = "xclip -o -selection"
        stdout = run_bash_completion(comp_line, __file__)
        self.assertEqual(stdout, "-selection", "\"{}\"".format(comp_line))

    def test_partial(self):
        # We have one letter of the word to work with. The only valid option
        # here should be "primary"
        comp_line = "xclip -o -selection p"
        stdout = run_bash_completion(comp_line, __file__)
        self.assertEqual(stdout, "primary", "\"{}\"".format(comp_line))


def completion_hook(cmd, curr_word, prev_word, comp_line, comp_point):
    potential_matches = []
    # Complete command options. The single-letter commands all start with the
    # same as their more verbose equivalents.
    if curr_word.startswith("-") or not curr_word:
        potential_matches = [
            "-in", "-out", "-loops", "-display", "-help", "-selection",
            "-noutf8", "-target", "-version", "-silent", "-quiet", "-verbose"
        ]

    # Complete options for selection.
    if prev_word == "-selection":
        potential_matches = ["buffer-cut", "clipboard", "primary", "secondary"]

    matches = [k for k in potential_matches if k.startswith(curr_word)]
    return matches


def main():
    helper(completion_hook)


if __name__ == "__main__":
    main()
