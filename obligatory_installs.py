#!/usr/bin/env python3
import argparse
import cmd
import json
import pathlib
import os
import shutil
import subprocess
import sys

# TODO: Redo this file, writing/copying files to /etc/profile.d
# if git is detected, the prompt should be adjusted to include $(__git_ps1).

# TODO: Include various apt installs:
# apt installs:
# build-essential ctags python3-dev tmux ffmpeg tree

# apt installs that are useful, but have lots of dependencies:
# graphviz
# 	Deps: fonts-liberation graphviz libann0 libcdt5 libcgraph6 libgd3 libgts-0.7-5 libgts-bin libgvc6 libgvpr2 liblab-gamut1 libpathplan4
# pandoc
#   Deps: pandoc-data
# asciinema:
#   Deps: ???
def append_to_profile():
    profile_path = pathlib.Path.home() / ".profile"
    profile_appendix_added = False
    with open(profile_path, "r") as f:
        lines = f.readlines()
        if "~/dotfiles/profile-appendix" in lines:
            profile_appendix_added = True
    if not profile_appendix_added:
        with open(profile_path, "a") as f:
            f.write(". ~/dotfiles/profile-appendix\n")


def install_vundle():
    bundle_path = pathlib.Path.home() / ".vim" / "bundle" / "Vundle.vim"
    if not bundle_path.exists():
        command = [
            "git", "clone", "https://github.com/VundleVim/Vundle.vim.git",
            str(bundle_path)
        ]
        try:
            print(" ".join(command))
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            raise e

def copy_vim_templates():
    source = pathlib.Path.home() / "dotfiles" / "vim" / "templates"
    destination = pathlib.Path.home() / ".vim" / "templates"
    shutil.copytree(str(source), str(destination), dirs_exist_ok=True)

def symlink_dotfiles():
    dotfiles = ["bash_aliases", "dircolors", "gitconfig", "tmux.conf", "vimrc"]
    for filename in dotfiles:
        symlink_path = pathlib.Path.home() / ("." + filename)
        if not symlink_path.exists():
            target = pathlib.Path() / "dotfiles" / filename
            symlink_path.symlink_to(target)
        else:
            print("{} exists. Skipping.".format(symlink_path))


def symlink_windows_user():
    cmd_exe = shutil.which("cmd.exe")
    if not cmd_exe:
        return
    process = subprocess.run(
        [cmd_exe, "/c", "echo", "%username%"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True
    )
    windows_user = process.stdout.strip()
    windows_user_path = pathlib.Path("/mnt/c/Users") / windows_user
    symlink_path = pathlib.Path.home() / "me"
    if not symlink_path.exists():
        symlink_path.symlink_to(windows_user_path)


def symlink_bin():
    bin_path = pathlib.Path.home() / "bin"
    if not bin_path.exists():
        bin_path.mkdir(parents=True)
    targets = pathlib.Path().home() / "dotfiles" / "bin"
    for target in targets.iterdir():
        symlink_path = bin_path / target.stem
        if not symlink_path.exists():
            symlink_path.symlink_to(target)
            symlink_path.chmod(0o777)


def silence_bell():
    inputrc = pathlib.Path.home() / ".inputrc"
    with open(inputrc, "w") as f:
        f.write("set bell-style none")



class PrintCompletionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("complete -C {} {}".format(__file__, __file__))
        parser.exit()


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bash-completion",
        nargs=0,
        action=PrintCompletionAction,
        help="Print completion code for bash"
    )

    parser.add_argument(
        "--tech-stack",
        action="store_true"
    )
    args = parser.parse_args()
    return args

def detect_tech_stack():
    summary = {}
    commands = {"git", "make"}
    for command in commands:
        summary[command] = shutil.which(command)

    return summary

def handle_completion():
    if os.environ.get("COMP_LINE") and os.environ.get("COMP_POINT"):
        parser = argparse.ArgumentParser()
        command, curr_word, prev_word = sys.argv[1:]
        matches = None
        if prev_word == command:
            matches = ["--tech-stack"]
        if matches:
            matches = [k for k in matches if k.startswith(curr_word)]
            print("\n".join(matches))
        quit()


class SymLinkerCmd(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "(SymLinker) "

    def do_link_dotfiles(self, args):
        symlink_dotfiles()

    def do_link_windows_user(self, args):
        symlink_windows_user()

    def do_symlink_bin(self, args):
        symlink_bin()

    def complete_include(self, text, line, begidx, endidx):
        return [str(_.name) for _ in self.common_profile_parts.iterdir()]

    def do_include(self, args):
        print(", ".join(args))

    def do_EOF(self, args):
        return True

def main():
    # It should be implied that you have git (needed to check this out)
    # It should also be implied you have a version of python to run it.
    handle_completion()
    if False:
        args = handle_args()
        if args.tech_stack:
            tech_stack = detect_tech_stack()
            print(json.dumps(tech_stack, sort_keys=True, indent=4))
        quit()
    append_to_profile()
    install_vundle()
    symlink_dotfiles()
    symlink_windows_user()
    symlink_bin()
    copy_vim_templates()
    silence_bell()


if __name__ == "__main__":
    main()
