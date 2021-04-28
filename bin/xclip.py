#!/usr/bin/env python3

# This is not actually xclip, but a makeshift subsitute for WSL since you
# don't have access to an X Display by default.
import subprocess
import sys

def copy(text):
    p = subprocess.Popen(
        ["/mnt/c/Windows/system32/clip.exe"],
        shell=True,
        stdin=subprocess.PIPE,
        close_fds=True
    )
    p.communicate(input=text.strip().encode("utf8"))


if __name__ == "__main__":
    copy(sys.stdin.read())
