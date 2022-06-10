#!/usr/bin/env python3
import itertools
from collections import Counter
import pathlib

def main():
    lines = None
    bash_history = pathlib.Path.home() / ".bash_history"
    with open(bash_history, "r") as f:
        lines = tuple(_.strip() for _ in f.readlines())
    counts = Counter(zip(lines, lines[1:]))
    for pairing in sorted(counts, key=counts.__getitem__, reverse=True):
        if counts[pairing] > 1:
            print(pairing, counts[pairing])

if __name__ == "__main__":
    main()

