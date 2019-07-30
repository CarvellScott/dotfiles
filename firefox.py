#!/usr/bin/env python3
import subprocess
import sys

def open_firefox(*args):
    str_args = list(map(str, *args))
    p = subprocess.Popen(
        " ".join(str_args),
        shell=True,
        stdin=subprocess.PIPE,
        close_fds=True
    )


class Fluent:
    def __init__(self, cache=None):
        self._cache = cache or []

    @classmethod
    def _from_parts(cls, args):
        return Fluent(args)

    def __truediv__(self, key):
        return self._from_parts(self._cache + [key])

    def url(self):
        return "https://" + "/".join(self._cache)

    def __str__(self):
        return self.url()

def main():
    firefox_executable = "/mnt/c/Program\ Files/Mozilla\ Firefox/firefox.exe"
    open_firefox([firefox_executable] + sys.argv[1:])
    if False:
        youtube = Fluent() / "youtu.be"
        open_firefox(youtube / "XYoTrI5RE-k")

if __name__ == "__main__":
    main()
