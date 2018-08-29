#!/usr/bin/env python3
import pathlib
import subprocess


def main():
    # Append the profile index if it's not there already
    profile_path = pathlib.Path.home() / ".profile"
    profile_appendix_added = False
    with open(profile_path, "r") as f:
        lines = f.readlines()
        if "~/dotfiles/profile-appendix" in lines[-1]:
            profile_appendix_added = True
    if not profile_appendix_added:
        with open(profile_path, "a") as f:
            f.write(". ~/dotfiles/profile-appendix\n")

    # Install Vundle for vim
    bundle_path = pathlib.Path.home() / ".vim" / "bundle"
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

    # Symlink dotfiles
    dotfiles = ["bash_aliases", "gitconfig", "tmux.conf", "vimrc"]
    for filename in dotfiles:
        symlink_path = pathlib.Path.home() / ("." + filename)
        if not symlink_path.exists():
            target = pathlib.Path() / "dotfiles" / filename
            symlink_path.symlink_to(target)
        else:
            print("{} exists. Skipping.".format(symlink_path))


if __name__ == "__main__":
    main()
