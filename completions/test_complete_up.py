#!/usr/bin/env python3
import unittest
from completion_helper import bash_complete

class CompletionTestCase_up(unittest.TestCase):
    def test_mnt(self):
        actual = bash_complete("asc mn", "/home/muhznit/dotfiles/completions/complete_up.py")
        expected = "/mnt"
        err = "Expected {}, got {}".format(expected, actual)
        self.assertEqual(actual, expected, err)

def main():
    unittest.main()


if __name__ == "__main__":
    main()
