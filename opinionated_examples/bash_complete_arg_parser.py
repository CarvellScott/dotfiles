#!/usr/bin/env python3
import argparse
import os
import sys


class BashCompleteArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _bash_complete_recursor(self, matches=None):
        if os.environ.get("COMP_LINE") and os.environ.get("COMP_POINT"):
            command, curr_word, prev_word = sys.argv[1:]
            comp_line = os.environ.get("COMP_LINE")

        matches = set()
        for action in self._actions:
            for opt_string in action.option_strings:
                if opt_string.startswith(curr_word):
                    matches.add(opt_string)
        return matches


    def parse_args(self):
        if os.environ.get("COMP_LINE") and os.environ.get("COMP_POINT"):
            matches = self._bash_complete_recursor()
            if matches:
                print("\n".join(matches))
            quit()
        return super().parse_args()


def get_arg_parser():
    description = (
        "This is intended to be an offline reference and demo for best "
        "practices for command-line arguments and flags using "
        "https://clig.dev/#arguments-and-flags as reference. It also includes "
        "a subclassed version of ArgumentParser that provides built-in bash "
        "completion."
    )

    parser = BashCompleteArgParser(description=description)
    parser.add_argument(
        "-c", "--config", type=pathlib.Path,
        help="Configuration file. Ideally something that supports shebangs."
    )
    # Opinion: Ideally a user should not have to debug a tool you wrote, so
    # don't necessarily show them debug output. DO however, create some file
    # they can send to you for debugging.
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="Enable debugging functions."
    )
    # Opinion: Dry runs should be built into interactive confirmations.
    parser.add_argument(
        "-f", "--force", action="count", default=0,
        help="Bypass confirmation for destructive actions."
    )
    # Opinion: The program should assume non-interactivity by default
    parser.add_argument(
        "-i", "--interactive", action="store_true",
        default=sys.stdin.isatty() and sys.stdout.isatty(),
        help="Allow interactive prompts"
    )
    parser.add_argument(
        "-o", "--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file. Output format should be derived from the filename"
    )
    # Opinion: Verbosity is best controlled via --quiet.
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Display less output."
    )

    parser.add_argument("-a", "--all", action="store_true", help="All.")
    parser.add_argument("-p", "--port", type=int, help="Port.")
    parser.add_argument("-u", "--user", type=str, help="User.")
    parser.add_argument(
        "-v", "--version", action="version",
        version="0.0.0"
    )
    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    print(args, file=sys.stderr)
    if args.interactive:
        user = input("Hello, what is your name?")
        print(f"Hello, {user}", file=args.output)
    else:
        print("Running non-interactively", file=sys.stderr)
    print(f"Output written to {args.output.name}")


if __name__ == "__main__":
    main()
