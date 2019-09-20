#!/usr/bin/env python3
import pathlib
import tempfile
import shlex
import subprocess
import os
import sys


def main():
    cwd = pathlib.Path.cwd()
    makefile_names = ("Makefile", "makefile", "GNUmakefile")
    makefiles = list([cwd / _ for _ in makefile_names])
    extension = pathlib.Path.home() /"dotfiles" / "Makefile"
    if "MAKEAPPENDS" in os.environ:
        appends = os.environ["MAKEAPPENDS"].split(":")
        appends = [pathlib.Path(_) for _ in appends]
        makefiles.extend(appends)
    else:
        print("MAKEAPPENDS is not set", file=sys.stderr)

    # Read list of files to fuse together.
    lines = list()
    for filepath in makefiles:
        if filepath.exists():
            with open(filepath, "r") as f:
                lines.extend(f.readlines())

    # Create the fused file and execute
    with tempfile.NamedTemporaryFile("w+") as named_file:
        named_file.write("".join(lines))
        named_file.seek(0)

        command = ["make", "-f", named_file.name] + sys.argv[1:]
        p = subprocess.Popen(command)
        p.communicate()

    #print(p.stdout.read())

if __name__ == "__main__":
    # main_split()
    main()
