#!/usr/bin/env python3.5
import sys


def xclip_completion(command, current_word, previous_word):
    if command != "xclip":
        return None

    potential_matches = []
    # Complete command options. The single-letter commands all start with the same as
    # their more verbose equivalents.
    if current_word.startswith("-"):
        potential_matches = [
            "-in", "-out", "-loops", "-display", "-help", "-selection",
            "-noutf8", "-target", "-version", "-silent", "-quiet", "-verbose"
        ]

    # Complete options for selection.
    if previous_word == "-selection":
        potential_matches = ["primary", "secondary", "clipboard", "buffer-cut"]

    matches = [k for k in potential_matches if k.startswith(current_word)]

    return "\n".join(matches)


def main():
    results = completion_hook(*sys.argv[1:])
    if results:
        print(results)


if __name__ == "__main__":
    main()
