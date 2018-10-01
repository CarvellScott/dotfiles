#!/usr/bin/env python3
import os
import pathlib
import sys

COMPLETION_SOURCE = """
if ! shopt -oq posix; then
    if [ -d $VIRTUAL_ENV/share/bash-completion/completions ]; then
        . $VIRTUAL_ENV/share/bash-completion/completions/*
    fi
fi
"""


def main():
    # Ensure we're working in a virtual environment
    venv_dir = pathlib.Path(os.environ.get("VIRTUAL_ENV"))
    if not venv_dir:
        raise FileNotFoundError("Not working in a virtual environment.")

    # Create the completion file if it doesn't exist.
    completion_filename = "venv_bash_completion"
    activate_script_path = venv_dir / "bin" / "activate"
    with open(venv_dir / "bin" / completion_filename, "w+") as f:
        f.write(COMPLETION_SOURCE)

    # Check that the file gets sourced upon environment activation.
    requires_install = False
    with open(activate_script_path, "r") as f:
        requires_install = (". %s" % (completion_filename)) not in f.read()

    # If not, make it so
    if requires_install:
        with open(activate_script_path, "a") as f:
            f.write("\n# Added via %s\n. %s" % (__file__, completion_filename))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        exit()
