#!/usr/bin/env python3
"""
This is kind of a sort of personal version of virtualenv_wrapper.
I wanted auto-completion of my virtualenvs and the ability to create them from
wherever but without having to install python2.7.
"""
import pathlib
import tempfile
import subprocess
import os
import sys
import venv

def handle_completion():
    if os.environ.get("COMP_LINE") and os.environ.get("COMP_POINT"):
        command, curr_word, prev_word = sys.argv[1:]
        if prev_word == command:
            p = pathlib.Path.home() / "venvs"
            words = [_.name for _ in p.glob(curr_word + "*")]
            print("\n".join(words))
        quit()


def main():
    handle_completion()
    venv_name = sys.argv[1]
    venvs_path = pathlib.Path.home() / "venvs"
    venv_path = venvs_path / venv_name
    venv_activate  = venv_path / "bin" / "activate"
    if not venv_path.exists():
        msg = "venv {} does not exist".format(str(venv_path))
        if sys.stdin.isatty():
            print(msg)
            create_venv = input("Create it? (y/n)")
            if "y" in create_venv:
                venv.create(venv_path)
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
