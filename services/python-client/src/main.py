from utils.helper_functions import ROOT_DIR
from utils.logging import setup_logger
from data_collection.data_collection import read_serial
from utils.config import config
import logging

logger = logging.getLogger('logger')

if __name__ == "__main__":
    setup_logger()
    while True:
        read_serial()
