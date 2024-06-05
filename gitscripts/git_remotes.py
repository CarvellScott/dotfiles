#!/usr/bin/env python3
import subprocess

def _get_remotes():
    output = subprocess.check_output(
        ("git", "remote", "show"),
        universal_newlines=True
    )
    for line in output.splitlines():
        yield line


def remote_to_url(remote_name):
    output = subprocess.check_output(
        ("git", "remote", "get-url", remote_name),
        universal_newlines=True
    )
    url = output.strip()
    return f"{remote_name}: {url}"


def main():
    for _ in sorted(_get_remotes()):
        print(remote_to_url(_))


if __name__ == "__main__":
    main()
