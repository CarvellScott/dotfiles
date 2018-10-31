#!/usr/bin/env python3
import shlex
import subprocess
import unittest
from completion_helper import helper


def run_completion(comp_line, completion_exe):
    cmd_line_args = shlex.split(comp_line)
    cmd = cmd_line_args[0]
    if comp_line.endswith(" "):
        curr_word = ""
        prev_word = cmd_line_args[-1]
    else:
        curr_word = cmd_line_args[-1]
        prev_word = cmd_line_args[-2]

    install_cmd = "complete -C {} {}".format(completion_exe, cmd)
    subshell_cmd = (
        '{install_cmd}; COMP_LINE="{comp_line}" COMP_POINT={comp_point} '
        '{completion_exe} {cmd} {curr_word} {prev_word}'
    ).format(
        **locals(),
        comp_point=len(comp_line)
    )

    out = subprocess.run(['bash', '-i', '-c', subshell_cmd],
        stdout=subprocess.PIPE, universal_newlines=True
    )
    return out.stdout


class BashTestCase(unittest.TestCase):
    def test_complete(self):
        comp_line = "xclip -selection p"
        completion_exe = "/$HOME/dotfiles/completions/complete_xclip.py"
        stdout = run_completion(comp_line, completion_exe)
        self.assertEqual(stdout, "primary\n", "\"{}\"".format(comp_line))

if __name__ == "__main__":
    unittest.main()
