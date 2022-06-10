#!/usr/bin/env python3
import argparse
import socket
import subprocess
import sys
import urllib.parse


def get_phone_repo_url():
    p = subprocess.run(
        "git remote get-url phone",
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    url = p.stdout.strip()
    return url


def set_remote_url(remote_name, url):
    p = subprocess.run(
        "git remote set-url {} {}".format(remote_name, url),
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )


def host_is_up(hostname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket.create_connection((hostname, 8022), timeout=3)
        sock.settimeout(None)
        return True
    except Exception as e:
        print("Host {} is unreachable: {}".format(hostname, e), file=sys.stderr)
    finally:
        sock.close()
    return False


def get_new_remote_url(hostname, url_pieces):
    netloc_parts = []
    if url_pieces.username:
        netloc_parts.append("{}@".format(url_pieces.username))
    netloc_parts.append(hostname)
    if url_pieces.port:
        netloc_parts.append(":{}".format(url_pieces.port))
    netloc = "".join(netloc_parts)
    replacement = url_pieces._replace(netloc=netloc)
    url = replacement.geturl()
    return url


def main():
    parser = argparse.ArgumentParser(
        description="Updates remote urls for phone-backed repositories."
    )
    parser.add_argument(
        "remote_host",
        type=str,
        nargs="?",
        help="Hostname or IP address for the desired remote host."
    )

    args = parser.parse_args()
    raw_remote_host = args.remote_host
    phone_repo_url = get_phone_repo_url()
    url_pieces = urllib.parse.urlparse(phone_repo_url)
    curr_remote_host = url_pieces.hostname

    if raw_remote_host is None:
        raw_remote_host = curr_remote_host

    raw_remote_host = raw_remote_host or curr_remote_host
    if not host_is_up(raw_remote_host):
        quit("No connectivity detected to {}".format(raw_remote_host))

    url = get_new_remote_url(raw_remote_host, url_pieces)
    if raw_remote_host != curr_remote_host:
        msg = "Change in host: {} -> {}".format(curr_remote_host, raw_remote_host)
        print(msg, file=sys.stderr)
        print("New url is {}".format(url), file=sys.stderr)
        set_remote_url("phone", url)
    else:
        msg = "Not changing current host ({})".format(curr_remote_host)
        print(msg, file=sys.stderr)


if __name__ == "__main__":
    main()
