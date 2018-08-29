#!/usr/bin/env python3
import pathlib
import zipfile


def main():
    blacklist = {"__pycache__", ".git"}
    path = pathlib.Path()
    files = filter(lambda i: str(i) not in blacklist, path.iterdir())
    files = filter(lambda i: ".swp" not in str(i), files)
    zipf = zipfile.ZipFile("dotfiles.zip", "w", zipfile.ZIP_DEFLATED)
    for i in files:
        zipf.write(i)
        print(i)
    zipf.close()


if __name__ == "__main__":
    main()
