#!/usr/bin/env python3
import argparse
import errno
import json
import os
import pathlib
import shlex
import subprocess
import sys

FIFO_PATH = "/tmp/completion_tester.fifo"


def helper(completion_function):
    # TODO: Support other shells.
    shell = os.environ.get("SHELL")
    if "bash" not in shell:
        quit("Sorry, only bash supported at the moment!")

    # Get arguments and environment variables
    try:
        comp_line = os.environ["COMP_LINE"]
        comp_point = os.environ["COMP_POINT"]
    except KeyError:
        # if the "COMP" variables aren't set, the script is being executed by
        # something other than complete. Assuming it's the user, we print up
        # some installation instructions that they can evaluate.
        script_path = pathlib.Path(sys.argv[0]).absolute()
        args = ["complete", "-C", str(script_path)]
        args.extend(sys.argv[1:])
        if sys.stdout.isatty():
            print("Redirect this into your .profile to install:", file=sys.stderr)
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
    if len(results):
        print("\n".join(results))
        print(json.dumps(comp_vars, indent=4), file=sys.stderr)


def run_bash_completion(comp_line, completion_exe):
    cmd_line_args = shlex.split(comp_line)
    cmd = cmd_line_args[0]
    if comp_line.endswith(" "):
        curr_word = ""
        prev_word = cmd_line_args[-1]
    else:
        curr_word = cmd_line_args[-1]
        prev_word = cmd_line_args[-2]

    # install cmd is what you execute in bash to install the completion
    install_cmd = "complete -C {} {}".format(completion_exe, cmd)

    # Summary of this command:
    # 1. Install the completion to the current shell environment
    # 2. Set environment variables used by completion
    # 3. Run the executable that's supposed to produce completion for
    # curr_word, supplying parameters in the same way complete does.
    subshell_cmd = (
        '{install_cmd}; COMP_LINE="{comp_line}" COMP_POINT={comp_point} '
        '{completion_exe} {cmd} {curr_word} {prev_word}'
    ).format(
        **locals(),
        comp_point=len(comp_line)
    )

    # That long mess of bash needs to be run in a subshell because bash is
    # weird about executing builtins.
    finished_process = subprocess.run(
        ['bash', '-i', '-c', subshell_cmd],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True
    )
    return finished_process.stdout.strip()


def main():
    # Any completion function wrapped by helper will generate output to be
    # written to a temporary fifo.
    # This will constantly try to read from the fifo.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "exe",
        help=("Path to an executable to be run. Its output will be used to"
              "generate completions"),
    )
    args, remaining_args = parser.parse_known_args()
    print(run_bash_completion(" ".join(remaining_args) + " ", args.exe))


if __name__ == "__main__":
    main()
