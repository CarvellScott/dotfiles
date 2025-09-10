#!/usr/bin/env python3
import argparse
import webbrowser

def main():
    desc="Open a url with a specific keyword. Intended to be used with vim's keywordprg"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("url", type=str)
    parser.add_argument("keyword", type=str)
    args = parser.parse_args()
    full_url = args.url + args.keyword
    webbrowser.open(full_url)

if __name__ == "__main__":
    main()

