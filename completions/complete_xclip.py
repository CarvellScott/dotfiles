#!/usr/bin/env python3
import unittest

try:
    import completion_utils
except:
    import df_completion_utils as completion_utils


class CompletionTestCase_xclip(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exe = __file__

    def assert_completion(self, comp_line, expected):
        stdout = completion_utils.bash_complete(comp_line, self.exe)
        err_template = "Expected {}, got {}"
        err = err_template.format(expected, stdout)
        self.assertEqual(stdout, expected, err)

    def test_end_with_space(self):
        # There's a space at the end of comp line, so display all options that
        # are applicable for the previous word.
        comp_line = "xclip -o -selection "
        expected = "buffer-cut\nclipboard\nprimary\nsecondary"
        self.assert_completion(comp_line, expected)

    def test_still_completing(self):
        # The word is still being completed, if there's another word that
        # starts with it, then that would be a viable completion option.
        comp_line = "xclip -o -selection"
        expected = "-selection"
        self.assert_completion(comp_line, expected)

    def test_partial_alt(self):
        # We have one letter of the word to work with. The only valid option
        # here should be "primary"
        comp_line = "xclip -o -selection p"
        expected = "primary"
        self.assert_completion(comp_line=comp_line, expected=expected)


class CompleteXClip(completion_utils.BashCompletion):
    def completion_hook(self, cmd, curr_word, prev_word):
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
            potential_matches = [
                "buffer-cut", "clipboard", "primary", "secondary"
            ]

        matches = [k for k in potential_matches if k.startswith(curr_word)]
        return matches


if __name__ == "__main__":
    CompleteXClip().main()
