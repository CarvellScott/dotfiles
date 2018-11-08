#!/usr/bin/env python3
import os
import pathlib
import shlex
import subprocess
import sys


def helper(completion_function):
    """
    ``completion_function`` is assumed to take 3 positional arguments and 2
    optional keyword arguments. In order, those are:
    command - The command the completion should be run for.
    current_word - The current word being typed at the terminal.
    previous_word - The previous word in the line.
    comp_line - The entire line of text entered at the terminal so far.
    comp_point - The cursor's index in the line entered at the terminal.
    completion_function should return an array of strings.
    """
    # TODO: Support other shells?
    shell = os.environ.get("SHELL")
    if "bash" not in shell:
        quit("Sorry, only bash supported at the moment!")

    comp_exe = str(pathlib.Path(sys.argv[0]).absolute())
    # Get arguments and environment variables
    try:
        comp_line = os.environ["COMP_LINE"]
        comp_point = os.environ["COMP_POINT"]
    except KeyError:
        # if the "COMP" variables aren't set, the script is being executed by
        # something other than complete. Assuming it's the user, we print up
        # some installation instructions that they can evaluate.
        args = ["complete", "-C", comp_exe]
        args.extend(sys.argv[1:])
        if sys.stdout.isatty():
            usr_msg = "Redirect this into your .profile to install:"
            print(usr_msg, file=sys.stderr)
        print(" ".join(args).strip())
        return

    cmd = sys.argv[1]
    curr_word = sys.argv[2] if len(sys.argv) > 3 else ""
    prev_word = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2]

    # Build up a dict of parameters for the completion function.
    comp_vars = dict(
        cmd=cmd,
        curr_word=curr_word,
        prev_word=prev_word,
        comp_line=comp_line,
        comp_point=comp_point
    )

    if completion_function:
        results = completion_function(**comp_vars)

    # bash reads stdout for completion. Each entry is on a new line.
    if len(results):
        print("\n".join(results))


def bash_complete(comp_line, comp_exe):
    """
    This is an approximation of how bash's complete function generates matches.
    ``comp_line`` Is the line assumed to be at the terminal.
    ``comp_exe`` is the path to an executable file that will generate matches.
    Returns the stdout of comp_exe after running with parameters normally
    supplied by complete.
    """
    cmd_line_args = shlex.split(comp_line)
    cmd = cmd_line_args[0]
    comp_point = str(len(comp_line))
    curr_word = ""
    prev_word = cmd
    if comp_line.endswith(" "):
        curr_word = ""
        prev_word = cmd_line_args[-1]
    else:
        curr_word = cmd_line_args[-1]
        prev_word = cmd_line_args[-2]

    os.environ.update({
        "COMP_LINE": comp_line,
        "COMP_POINT": comp_point
    })
    finished_process = subprocess.run(
        [comp_exe, cmd, curr_word, prev_word],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return finished_process.stdout.strip()


if __name__ == "__main__":
    if len(sys.argv) > 1 and pathlib.Path(sys.argv[1]).exists():
        print(bash_complete(" ".join(sys.argv[2:]), sys.argv[1]))
    else:
        print("usage: completion_helper executable line", file=sys.stderr)
