import os
import sys
import logging
from utils.helper_functions import ROOT_DIR
from dotenv import load_dotenv
load_dotenv(f"{ROOT_DIR}/../.env")

logger = logging.getLogger('logger')


class config:
    COM_PORT = os.getenv("COM_PORT")
    BAUD_RATE = os.getenv("BAUD_RATE")
    WRITE_ARUDINO_DATA = os.getenv("WRITE_ARUDINO_DATA").lower().capitalize() == "True"
    PRODUCT_CODE = os.getenv("PRODUCT_CODE")
    BASE_SERVER_URL = os.getenv("BASE_SERVER_URL")
