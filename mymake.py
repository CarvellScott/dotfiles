#!/usr/bin/env python3
import pathlib
import tempfile
import shlex
import subprocess
import os
import sys


def _get_fused_makefile_text():
    cwd = pathlib.Path.cwd()
    makefile_names = ("Makefile", "makefile", "GNUmakefile")
    makefiles = []
    for _ in makefile_names:
        possible_makefile = cwd / _
        if possible_makefile.exists():
            makefiles.append(possible_makefile)
            break

    if "MAKEAPPENDS" in os.environ:
        appends = os.environ["MAKEAPPENDS"].split(":")
        appends = [pathlib.Path(_) for _ in appends]
        makefiles.extend(appends)
    else:
        print("MAKEAPPENDS is not set", file=sys.stderr)

    lines = list()
    for filepath in makefiles:
        if filepath.exists():
            with open(filepath, "r") as f:
                lines.extend(f.readlines())

    return "".join(lines)

def main():
    # Read list of files to fuse together.
    fused_makefile_text = _get_fused_makefile_text()
    print(fused_makefile_text)
    if "COMP_LINE" in os.environ:
        command, curr_word, prev_word = sys.argv[1:]
        lines = fused_makefile_text.splitlines()
        lines = map(lambda _: re.match(r"^(\S+):", _), lines)
        lines = filter(lambda _: bool(_), lines)
        lines = map(lambda _: _.group(1), lines)
        lines = filter(lambda _: not _.startswith("."), lines)
        matches = {_ for _ in targets if _.startswith(curr_word)}
        if matches:
            print("\n".join(matches))
        quit()

    # Create the fused file and execute
    with tempfile.NamedTemporaryFile("w+") as named_file:
        named_file.write(fused_makefile_text)
        named_file.seek(0)

        command = ["make", "-f", named_file.name] + sys.argv[1:]
        p = subprocess.Popen(command)
        p.communicate()

    #print(p.stdout.read())

if __name__ == "__main__":
    # main_split()
    main()
