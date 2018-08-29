#!/usr/bin/env python3
import subprocess


def get_remotes():
    p = subprocess.run(
        "git remote show",
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    remote_names = p.stdout.splitlines()
    return remote_names


def remote_to_url(remote_name):
    p = subprocess.run(
        "git remote get-url {}".format(remote_name),
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    url = p.stdout.strip()
    return remote_name, url


def main():
    remote_names = map(remote_to_url, get_remotes())
    remote_names = dict(remote_names)
    remote_names = map(lambda i: "{}: {}".format(*i), remote_names.items())
    remote_names = list(remote_names)
    remote_names.sort()
    print("\n".join(remote_names))


if __name__ == "__main__":
    main()
