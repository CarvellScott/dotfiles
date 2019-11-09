#!/usr/bin/env python3
import pathlib
import re

try:
    import completion_utils
except (ImportError, ModuleNotFoundError):
    import df_completion_utils as completion_utils


class CompleteUp(completion_utils.BashCompletion):
    def completion_hook(self, command, curr_word, prev_word):
        matches = []
        try:
            curr_path = pathlib.Path().absolute()
        except FileNotFoundError:
            curr_path = pathlib.Path.home().absolute()

        paths = list(curr_path.parents)
        if curr_path == pathlib.Path.home():
            paths += [curr_path]

        # Greedy regexes will match the path closest to curr_path
        paths = map(str, paths)
        regex = re.compile(r".*{}".format(re.escape(curr_word)))
        matches = {s for s in paths if regex.search(s)}
        return matches


if __name__ == "__main__":
    CompleteUp().main()
