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
        curr_path = pathlib.Path().absolute()

        # Greedy regexes will match the path closest to curr_path
        paths = map(str, curr_path.parents)
        regex = re.compile(r".*{}".format(re.escape(curr_word)))
        matches = {s for s in paths if regex.search(s)}
        return matches


if __name__ == "__main__":
    CompleteUp().main()
