#!/usr/bin/env python3
import errno
import json
import os
import shlex
import sys

FIFO_PATH = "/tmp/completion_tester.fifo"


def helper(completion_function):
    # TODO: Support other shells.
    shell = os.environ.get("SHELL")
    if "bash" not in shell:
        quit("Sorry, only bash supported at the moment!")

    # Get arguments and environment variables
    try:
        cmd = sys.argv[1]
        curr_word = sys.argv[2]
        prev_word = sys.argv[3]
        comp_line = os.environ["COMP_LINE"]
        comp_point = os.environ["COMP_POINT"]
    except (IndexError, KeyError):
        # if the "COMP" variables aren't set, the script is being executed by
        # something other than complete. Assuming it's the user, we print up
        # some installation instructions that they can evaluate.
        args = ["complete", "-C"]
        args.extend(sys.argv[:2])
        print("Redirect this into your .bashrc to install:", file=sys.stderr)
        print(" ".join(args).strip())
        return

    # Build up a dict of parameters for the completion function.
    comp_vars = dict(
        cmd=cmd,
        curr_word=curr_word,
        prev_word=prev_word,
        comp_line=comp_line,
        comp_point=comp_point
    )

    # completion_function is assumed to take 3 positional arguments and 2
    # optional keyword arguments. In order, those are:
    # command - The command the completion should be run for.
    # current_word - The current word being typed at the terminal.
    # previous_word - The previous word in the line.
    # comp_line - The entire line of text entered at the terminal so far.
    # comp_point - The cursor's index in the line entered at the terminal.
    # completion_function should return an array of strings.
    if completion_function:
        results = completion_function(**comp_vars)

    # bash reads stdout for completion. Each entry is on a new line.
    results = [shlex.quote(i) for i in results]
    if len(results):
        print("\n".join(results))

    # Write the contents to a fifo. Should probably use actual logging.
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)
    try:
        f = os.open(FIFO_PATH, os.O_WRONLY | os.O_NONBLOCK)
        os.write(f, bytes(json.dumps(comp_vars, indent=4), "utf-8"))
        os.close(f)
    except OSError as exc:
        if exc.errno == errno.ENXIO:
            pass
        else:
            print(exc, file=sys.stderr)
            raise


def main():
    # Any completion function wrapped by helper will generate output to be
    # written to a temporary fifo.
    # This will constantly try to read from the fifo.
    while True:
        try:
            with open(FIFO_PATH, "r") as f:
                print(f.read())
            os.unlink(FIFO_PATH)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()
