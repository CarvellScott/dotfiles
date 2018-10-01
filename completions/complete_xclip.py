#!/usr/bin/env python3
from completion_helper import helper


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
        potential_matches = ["primary", "secondary", "clipboard", "buffer-cut"]

    matches = [k for k in potential_matches if k.startswith(curr_word)]
    return matches


def main():
    helper(completion_hook)


if __name__ == "__main__":
    main()
