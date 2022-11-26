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
    LOG_LEVEL = logging.INFO
    if os.getenv("LOG_LEVEL").lower() == 'error':
        LOG_LEVEL = logging.ERROR
    elif os.getenv("LOG_LEVEL").lower() == 'warning':
        LOG_LEVEL = logging.WARNING
    elif os.getenv("LOG_LEVEL").lower() == 'info':
        LOG_LEVEL = logging.INFO
    elif os.getenv("LOG_LEVEL").lower() == 'debug':
        LOG_LEVEL = logging.DEBUG
