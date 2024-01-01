#!/usr/bin/env python3
import logging


def add_quickfix_handler(logger):
    fmt = '%(pathname)s:%(lineno)d: [%(levelname)-8s] %(message)s'
    formatter = logging.Formatter(fmt)
    handler = logging.FileHandler("quickfix.txt", "w")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

def set_up_logging(logger):
    logging_config = {
        "format": "%(asctime)s [%(levelname)-8s] %(filename)s:%(lineno)d: %(message)s",
        "datefmt": "%F %T"
    }
    logging.basicConfig(**logging_config)
    logger.setLevel(logging.INFO)

def main():
    log = logging.getLogger(__name__)
    set_up_logging(log)
    add_quickfix_handler(log)
    log.info("Logging has been set up")
    log.warning("Something has gone wrong that may lead to an error.")
    log.error("An error has occurred, but the program is still able to run")
    try:
        raise Exception("This is an exception.")
    except Exception as e:
        log.exception("An exception was intercepted.")
    log.fatal("If you see this, something catastrophic has occurred.")
    log.debug("This is debug level, probably shouldn't have too many of these")

if __name__ == "__main__":
    main()
