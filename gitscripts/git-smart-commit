#!/usr/bin/env python3
import subprocess
import os

SMART_COMMIT_MSG_FILENAME = ".git/COMMIT_EDITMSG"

def get_staged_paths():
    process_results = subprocess.run(
        "git diff --cached --name-only",
        stdout=subprocess.PIPE, shell=True
    )
    paths = process_results.stdout.decode().strip().splitlines()
    return paths


def git_commit(filename=SMART_COMMIT_MSG_FILENAME, dry_run=False):
    dry_run_opt = "--dry-run" if dry_run else ""
    process_results = subprocess.run(
        "git commit {} -F {}".format(dry_run_opt, filename),
        stdout=subprocess.PIPE, shell=True
    )
    return process_results.stdout.decode().strip()


def main():
    """
    The idea behind this script is that you can work on a big commit, add patch
    notes as you go, and when the time comes to commit, you don't have to worry
    about committing something newer than the commit message.
    """
    smart_commit_msg_filename = SMART_COMMIT_MSG_FILENAME
    paths = get_staged_paths()
    if not len(paths):
        raise Exception("did you even add anything to staging")
    paths += [smart_commit_msg_filename]
    mr_edited_file = max(paths, key=lambda k: os.path.getmtime(k))
    if mr_edited_file == smart_commit_msg_filename:
        print(git_commit())
    else:
        print("Update the patch notes!")


if __name__ == "__main__":
    main()
