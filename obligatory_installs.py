#!/usr/bin/env python3
import argparse
import cmd
import pathlib
import os
import subprocess

# TODO: Redo this file, taking more of a "build every file dynamically"
# approach. Specifically, it should accept a technology stack as a parameter
# and build config files as appropriate. For example, if "git" is supplied,
# the prompt is adjusted to include $(__git_ps1).

def append_to_profile():
    profile_path = pathlib.Path.home() / ".profile"
    profile_appendix_added = False
    with open(profile_path, "r") as f:
        lines = f.readlines()
        if "~/dotfiles/profile-appendix" in lines[-1]:
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
    process = subprocess.run(
        ["cmd.exe", "/c", "echo", "%username%"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True
    )
    windows_user = process.stdout.strip()
    windows_user_path = pathlib.Path("/mnt/c/Users") / windows_user
    symlink_path = pathlib.Path.home() / "me"
    if not symlink_path.exists():
        symlink_path.symlink_to(windows_user_path)


def symlink_bin():
    binaries = ["firefox", "xclip"]
    for bin_name in binaries:
        py_name = bin_name + ".py"
        symlink_path = pathlib.Path.home() / "bin" / bin_name
        if not symlink_path.exists():
            target = pathlib.Path().home() / "dotfiles" / py_name
            symlink_path.symlink_to(target)
            symlink_path.chmod(0o777)

class ProfileComposerCmd(cmd.Cmd):
    common_profile_parts = pathlib.Path.cwd() / "common_profile_parts"
    def __init__(self):
        super().__init__()
        self.wip_profile = ""

    def complete_include(self, text, line, begidx, endidx):
        return [str(_.name) for _ in self.common_profile_parts.iterdir()]

    def do_include(self, args):
        print(", ".join(args))

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
        "tech_stack",
        nargs="+",
        choices={"git", "make", "hg"},
        type=str
    )
    args = parser.parse_args()
    print(args)


def handle_completion():
    if os.environ.get("COMP_LINE") and os.environ.get("COMP_POINT"):
        parser = argparse.ArgumentParser()
        completion_params = ("command", "curr_word", "prev_word")
        for arg in completion_params:
            parser.add_argument(arg, type=str)
        args = parser.parse_args()
        print(args.__dict__)
        quit()

def main():
    handle_completion()
    handle_args()
    ProfileComposerCmd().cmdloop()
    quit()
    append_to_profile()
    install_vundle()
    symlink_dotfiles()
    symlink_windows_user()
    symlink_bin()


if __name__ == "__main__":
    main()
