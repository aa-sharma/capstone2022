import serial
import csv
from datetime import datetime
from utils.helper_functions import ROOT_DIR
import logging
from utils.config import config

logger = logging.getLogger('logger')

ser = serial.Serial(config.COM_PORT, config.BAUD_RATE)


def read_serial():
    data = ser.readLine()
    logger.debug(data)
    if config.WRITE_ARUDINO_DATA:
        __savefile(data)

    return data


def __savefile(data):
    # a functin for simply saving files
    with open(f'{ROOT_DIR}/../data/arduino_data.csv', "w+", newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(data)
