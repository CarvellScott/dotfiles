#!/usr/bin/env python3
import re
import subprocess
import datetime


def create_command(when):
    command = "git log --reverse --author=$(git config user.email) --date=short --since={}".format(when)
    return command


def get_ppp_since(command):
    process_results = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    output = process_results.stdout.decode().strip()
    return output
    lines = output.splitlines()
    lines = [re.sub(r"^ +", "", line) for line in lines]
    lines = [line for line in lines if line]
    output = "\n".join(lines[6:])
    return output


if __name__ == "__main__":
    today = str(datetime.date.today() - datetime.timedelta(days=6))
    cmd = create_command(today)
    output = get_ppp_since(cmd)
    print(output)
