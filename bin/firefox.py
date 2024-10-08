#!/usr/bin/env python3

# A makeshift way to open up firefox, since currently symlinking windows
# executables is broken.
import subprocess
import sys
import shlex

def open_firefox(*args):
    str_args = list(map(str, *args))
    p = subprocess.Popen(
        " ".join(str_args),
        shell=True,
        stdin=subprocess.PIPE,
        close_fds=True
    )


def main():
    firefox_executable = "/mnt/c/Program\ Files/Mozilla\ Firefox/firefox.exe"
    subprocess_args = sys.argv
    # Make sure urls with parameters are properly quoted
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue
        subprocess_args[i] = shlex.quote(arg)

    open_firefox([firefox_executable] + sys.argv[1:])

if __name__ == "__main__":
    main()
