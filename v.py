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
    venvs_path = pathlib.Path.home() / "venvs"
    venv_path = venvs_path / venv_name
    venv_activate  = venv_path / "bin" / "activate"
    if not venv_path.exists():
        raise Exception("venv {} does not exist".format(str(venv_path)))
    venv_activate = str(venv_activate)
    # Create the fused file and execute
    tmp_rc_content = (
        "#!/bin/bash\n"
        "source ~/.profile\n"
        "source {venv_activate}\n"
    ).format(**locals())
    with tempfile.NamedTemporaryFile("w+") as named_file:
        named_file.write(tmp_rc_content)
        named_file.seek(0)

        command = ["/bin/bash", "--rcfile", named_file.name]
        p = subprocess.Popen(command)
        p.communicate()


if __name__ == "__main__":
    main()
