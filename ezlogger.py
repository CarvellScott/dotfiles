#!/usr/bin/env python3
import json
import logging
import time


LOGFILENAME = __name__


def formatTime(record, datefmt=None):
    # Alternative useful formats for debugging purposes:
    # return "{}ms".format(record.relativeCreated)
    # return "{:10.5f}".format(record.created)
    iso_8601 = time.strftime("%F %T", time.localtime(record.created))
    return "{}.{}".format(iso_8601, int(record.msecs))


class VanillaFormatter(logging.Formatter):
    def format(self, record):
        return "{} {}:{} {} {}".format(
            formatTime(record),
            record.filename, record.lineno,
            record.levelname,
            record.getMessage()
        )

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#file_handler = logging.FileHandler("{}.log".format(LOGFILENAME))
ch = logging.StreamHandler()
ch.setFormatter(VanillaFormatter())

logger.addHandler(ch)


def get():
    return logger


if __name__ == "__main__":
    some_data = {
        "data": "data_irl",
        "more_data": [
            "nested",
            "shenanigans"
        ]
    }
    get().info(json.dumps(some_data))
    get().info("This is just a string, not your fancy \"json\" or anything.")
    get().debug("Just")
    get().info("Testing")
    get().warning("Different")
    get().error("Log")
    get().critical("Levels")
