from utils.helper_functions import ROOT_DIR
from utils.logging import setup_logger
from data_collection.data_collection import read_serial
from utils.config import config
import logging

logger = logging.getLogger('logger')
setup_logger()

if __name__ == "__main__":
    logger.info("Starting Data Processor")

    while True:
        read_serial()
