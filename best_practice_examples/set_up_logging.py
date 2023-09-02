#!/usr/bin/env python3
import logging

_LOG = logging.getLogger(__name__)

def set_up_logging():
    logging_config = {
        "format": "%(asctime)s [%(levelname)s] %(module)s:%(lineno)d:%(message)s",
        "datefmt": "%F %T"
    }
    logging.basicConfig(**logging_config)
    if False:
        quickfix_handler = logging.FileHandler("quickfix.txt", "w")
        fmt = '%(pathname)s:%(lineno)d:%(message)s'
        formatter = logging.Formatter(fmt, logging_config["datefmt"])
        quickfix_handler.setFormatter(formatter)
        quickfix_handler.setLevel(logging.WARNING)
        _LOG.addHandler(quickfix_handler)
    _LOG.setLevel(logging.DEBUG)

if __name__ == "__main__":
    set_up_logging()
    _LOG.info("Logging has been set up")
    _LOG.warning("Something has gone wrong that may lead to an error.")
    _LOG.error("An error has occurred, but the program is still able to run")
    _LOG.fatal("If you see this, something catastrophic has occurred.")
    _LOG.debug("This is debug level, probably shouldn't have too many of these")

