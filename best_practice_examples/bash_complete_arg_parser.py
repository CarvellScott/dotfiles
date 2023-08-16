#!/usr/bin/env python3
import argparse
import datetime
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


    def bash_complete_handler(self):
        if os.environ.get("COMP_LINE") and os.environ.get("COMP_POINT"):
            matches = self._bash_complete_recursor()
            if matches:
                print("\n".join(matches))
            quit()


def get_arg_parser():
    description = (
        "This is intended to be an offline reference and demo for best "
        "practices for command-line arguments and flags using "
        "https://clig.dev/#arguments-and-flags as reference. It also includes "
        "a subclassed version of ArgumentParser that provides built-in bash "
        "completion."
    )

    parser = BashCompleteArgParser(description=description)
    parser.add_argument("-a", "--all", action="store_true", help="All.")
    parser.add_argument("--after", type=datetime.datetime.fromisoformat,
                        help="After.")
    parser.add_argument("--before", type=datetime.datetime.fromisoformat,
                        help="Before.")
    parser.add_argument(
        "-c", "--csv", action="store_true",
        help="Display csv output."
    )
    # Opinion: Ideally a user should not have to debug a tool you wrote. This
    # also should probably be mutually exclusive with -q
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="Show debugging output."
    )
    # Destructiveness of a script should be a scale of 0-2:
    # 0: Change nothing, only print what will be done.
    # 1: Perform "normal" actions
    # 2: FLYYY MEEE TOOO THE DANGER ZONE!
    destructiveness = parser.add_mutually_exclusive_group()
    destructiveness.add_argument(
        "--dry-run", action="store_true",
        help="Print what will be done without actually doing it."
    )
    destructiveness.add_argument(
        "-f", "--force", action="store_true",
        help="Bypass confirmation for destructive actions."
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Display JSON output."
    )
    # Opinion: "-i/--interactive" is better, but if a person is using a CLI,
    # the program should be interactive by default.
    parser.add_argument(
        "-n", "--no-input", action="store_false",
        default=sys.stdin.isatty() and sys.stdout.isatty(),
        help="Do not use interactive prompts."
    )
    parser.add_argument(
        "-o", "--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file. Output format should be derived from this."
    )
    parser.add_argument(
        "-p", "--port", type=int,
        help="Port."
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Display less output."
    )
    parser.add_argument(
        "-u", "--user", type=str,
        help="User."
    )
    # Opinion: Verbosity is best controlled via --quiet.
    parser.add_argument(
        "-v", "--version", action="version",
        version="Unversioned"
    )
    return parser


def main():
    parser = get_arg_parser()
    parser.bash_complete_handler()
    args = parser.parse_args()
    if args.no_input:
        user = input("Hello, what is your name?")
        print(f"Hello, {user}", file=args.output)
    else:
        print("Running non-interactively", file=sys.stderr)
    print(f"Output written to {args.output.name}")


if __name__ == "__main__":
    main()
