#!/usr/bin/env python3
import pathlib
import tempfile
import shlex
import subprocess
import os
import sys


def main_split(filename):
    command = ["vi", "-u", filename]
    p = subprocess.Popen(command)
    p.communicate()

def main():
    original = pathlib.Path.home() / ".vimrc"
    extension = pathlib.Path.home() /"dotfiles" / "vimrc_ext"

    # Read list of files to fuse together.
    lines = list()
    for filepath in [original, extension]:
        with open(filepath, "r") as f:
            lines.extend(f.readlines())

    # Create the fused file and execute
    with tempfile.NamedTemporaryFile("w+") as named_file:
        named_file.write("".join(lines))
        named_file.seek(0)

        command = ["vi", "-u", named_file.name] + sys.argv[1:]
        p = subprocess.Popen(command)
        p.communicate()
        #main_split(named_file.name)

    #print(p.stdout.read())

if __name__ == "__main__":
    # main_split()
    main()
