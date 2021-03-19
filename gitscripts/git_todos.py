#!/usr/bin/env python3
import itertools
import json
import re
import subprocess


def get_blame_cmd(filename):
    cmd = "git blame --line-porcelain {}"
    return cmd.format(filename)


def get_todos(filename):
    p = subprocess.run(
        get_blame_cmd(filename),
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    lines = [line for line in p.stdout.splitlines() if not
             line.startswith("previous")]

    # Each entry, without the "previous" line, has 12 lines of data.
    lpe = 12
    entries = len(lines) // lpe
    todos_for_file = []
    for i in range(entries):
        # details contains every line of data for a given entry.
        details = lines[i * lpe:i * lpe + lpe]
        (commit, author, author_mail, author_time, author_tz,
         commiter, commiter_mail, committer_time, commiter_tz,
         summary, commit_filename, code) = details

        todo = re.search(r"# ?TODO.*", code)
        if todo:
            todos_for_file += [{
                "author_mail": author_mail[author_mail.find(" ") + 1:],
                "line": commit.split()[2],
                "filename": filename,
                "todo": todo.group(0)
            }]
    return todos_for_file


def main():
    command = "git ls-tree --name-only -r HEAD"
    p = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )

    file_list = [l for l in p.stdout.strip().splitlines() if l]
    todos_per_file = map(get_todos, file_list)
    todos_per_file = filter(lambda i: i, todos_per_file)
    todos = itertools.chain(*todos_per_file)
    template = "{filename}:{line}: {todo}"
    # TODO: Add an option to sort TODOs by age?
    todos = map(lambda i: template.format(**i), todos)
    print("\n".join(todos))


if __name__ == "__main__":
    main()
