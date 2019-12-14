#!/usr/bin/env python3
import pathlib
import tempfile
import subprocess
import os
import sys

def handle_completion():
    if os.environ.get("COMP_LINE") and os.environ.get("COMP_POINT"):
        command, curr_word, prev_word = sys.argv[1:]
        if prev_word == command:
            p = pathlib.Path.home() / "venvs"
            dirs = [_.name for _ in p.iterdir()]
            words = [_ for _ in dirs if _.startswith(curr_word)]
            print("\n".join(words))
        quit()


def main():
    handle_completion()
    venv_name = sys.argv[1]
    venv_path = pathlib.Path.home() / "venvs" / venv_name / "bin" / "activate"
    venv_path = str(venv_path)
    # Create the fused file and execute
    tmp_rc_content = (
        "#!/bin/bash\n"
        "source ~/.profile\n"
        "source {venv_path}\n"
    ).format(**locals())
    with tempfile.NamedTemporaryFile("w+") as named_file:
        named_file.write(tmp_rc_content)
        named_file.seek(0)

        print(named_file.name, file=sys.stderr)
        command = ["/bin/bash", "--rcfile", named_file.name]
        p = subprocess.Popen(command)
        p.communicate()


if __name__ == "__main__":
    main()
