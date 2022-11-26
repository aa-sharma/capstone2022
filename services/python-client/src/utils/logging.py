import os
import sys
from utils.helper_functions import ROOT_DIR
from logging.handlers import RotatingFileHandler
import logging
from utils.config import config

logger = logging.getLogger('logger')


class __CLIFormat(logging.Formatter):

    light_blue = "\x1b[36;20m"
    blue = "\x1b[36;1m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] [%(levelname)s] : %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: light_blue + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger():
    os.system(f'mkdir -p {ROOT_DIR}/../logs')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(__CLIFormat())

    file_format = logging.Formatter("[%(asctime)s] [%(levelname)s] : %(message)s (%(filename)s:%(lineno)d)")
    rotating_file_handler = RotatingFileHandler(
        f'{ROOT_DIR}/../logs/data_processor.log', maxBytes=200000, backupCount=10)
    rotating_file_handler.setFormatter(file_format)

    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.addHandler(stream_handler)
    logger.addHandler(rotating_file_handler)
    logger.setLevel(config.LOG_LEVEL)
