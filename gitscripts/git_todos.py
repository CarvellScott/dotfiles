#!/usr/bin/env python3
import subprocess

def main():
    command = "git grep -nor '# \?TODO.*'"
    p = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    print(p.stdout.strip())

if __name__ == "__main__":
    main()
