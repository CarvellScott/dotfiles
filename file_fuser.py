#!/usr/bin/env python3
import time
import errno
import json
import os
import shlex
import sys

FIFO_PATH = "/home/rudo3163/dotfiles/fusedvimrc"


"""
f = os.open(FIFO_PATH, os.O_WRONLY | os.O_NONBLOCK)
os.write(f, bytes(json.dumps(comp_vars, indent=4), "utf-8"))
os.close(f)
"""

def main():
    # Any completion function wrapped by helper will generate output to be
    # written to a temporary fifo.
    # This will constantly try to read from the fifo.
    while True:
        if os.path.exists(FIFO_PATH):
            os.unlink(FIFO_PATH)
        os.mkfifo(FIFO_PATH)
        try:
            with open(FIFO_PATH, "w") as f:
                with open("vimrc", "r") as vimrc:
                    f.write(vimrc.read() + "\n")
                f.write("colorscheme darkblue\n")
        except BrokenPipeError:
            pass

if __name__ == "__main__":
    main()
