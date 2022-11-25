import serial
import csv
from datetime import datetime
from utils.helper_functions import ROOT_DIR
import logging
from utils.config import config
import re
from data_processor import dataProcessor

logger = logging.getLogger('logger')

ser = serial.Serial(config.COM_PORT, config.BAUD_RATE)

def read_serial():
    """
    Reading from Arduino serial port.
    5 Values are appended to angleDict (index 0-4)
        [0] -> Pinky angle
        [1] -> Ring angle
        [2] -> Middle angle
        [3] -> Index angle
        [4] -> Thumb angle
        [5]* -> Roll
        [6]* -> Pitch
        [7]* -> Yaw
    *[TODO] Validate gyroscope x,y,z (fifth key value pair)
    This list is then passed to xxxx()

    Returns: Dictionary with 8 entries all of which are angles.
    """
    angleDict = {
        0 : {"Angle" : "0"},
        1 : {"Angle" : "0"},
        2 : {"Angle" : "0"},
        3 : {"Angle" : "0"},
        4 : {"Angle" : "0"},
        5 : {"Angle" : "0"},
        6 : {"Angle" : "0"},
        7 : {"Angle" : "0"}
    }  
    for x in range(5):
        ser = serial.Serial('/dev/tty.usbmodem1301', 9600, timeout = 1)
        input = ser.readline()
        ser.close()
        angleDict[x]["Angle"] = parseData(input)

        logger.debug(angleDict[x]["Angle"])
        if config.WRITE_ARUDINO_DATA:
            __savefile(angleDict[x]["Angle"])

    return angleDict

def parseData(inputData):
    """
    Function to extract just the angle data from received string from serial port.
    """
    print(str(inputData))
    adc = re.search("(\d+)", str(inputData))
    if adc:
        return adc.group(1)
    else:
        print(["[ERROR]: Could not parse input data."])

def repackageCartesian(XYZ):
    """
    [TODO] This function is to get the data into a format that is comprehensible to the web client. x,y,z for each point needs to be concatenated.
    Called after the angle to xyz conversion.
    """
    pass

def updateCartesianValues(angleDict):
    """
    Updates a nested dictionary of 22 entries each for a data point. 
    Map to keep track of idx and associated data point ex. pinkyA
    +----------+----------------------+
    | Index    |      Point Map       |
    +----------+----------------------+
    |    1     |        pinky A       |
    |    2     |        pinky B       |
    |    3     |        pinky C       |
    |    4     |        pinky D       |
    |    5     |        ring A        |
    |    6     |        ring B        |
    |    7     |        ring C        |
    |    8     |        ring D        |
    |    9     |        middle A      |
    |    10    |        middle B      |
    |    11    |        middle C      |
    |    12    |        middle D      |
    |    13    |        index A       |
    |    14    |        index B       |
    |    15    |        index C       |
    |    16    |        index D       |
    |    17    |        thumb A       |
    |    18    |        thumb B       |
    |    19    |        thumb C       |
    |    20    |        thumb D       |
    |    21    |           o          |
    |    22    |           W          |
    |    23    |     acceleration     |
    +----------+----------------------+
    TODO
    This function should only be called after passing the data to convert from angle to cartesian.
    Function to convert angles for each finger to data points (4 per finger).
    Mapping Algorithm (blurb):
        1. Define 0 and 180 for all fingers
        2. Define function to translate [x,y,z] based on angles.
    Passes mapped values to updateCartesianValues().
    """

    # Initial coordinates
    allPoints = {
        0 : {"x": "7", "y": "0", "z": "3"},
        1 : {"x": "3", "y": "2", "z": "9"},
        2 : {"x": "8", "y": "8", "z": "8"},
        3 : {"x": "1", "y": "6", "z": "1"},
        4 : {"x": "1", "y": "6", "z": "1"},
        5 : {"x": "1", "y": "6", "z": "1"},
        6 : {"x": "7", "y": "0", "z": "3"},
        7 : {"x": "3", "y": "2", "z": "9"},
        8 : {"x": "8", "y": "8", "z": "8"},
        9 : {"x": "1", "y": "6", "z": "1"},
        10 : {"x": "1", "y": "6", "z": "1"},
        11 : {"x": "1", "y": "6", "z": "1"},
        12 : {"x": "8", "y": "8", "z": "8"},
        13 : {"x": "1", "y": "6", "z": "1"},
        14 : {"x": "1", "y": "6", "z": "1"},
        15 : {"x": "1", "y": "6", "z": "1"},
        16 : {"x": "7", "y": "0", "z": "3"},
        17 : {"x": "3", "y": "2", "z": "9"},
        18 : {"x": "8", "y": "8", "z": "8"},
        19 : {"x": "1", "y": "6", "z": "1"},
        20 : {"x": "1", "y": "6", "z": "1"},
        21 : {"x": "1", "y": "6", "z": "1"},
        22 : {"x": "1", "y": "6", "z": "1"}
    }

    for i in range (5):
        x = angleDict[i]["ADC"]
        y = angleDict[i]["ADC"]
        z = angleDict[i]["ADC"]

        allPoints[i]["x"] = x
        allPoints[i]["y"] = y
        allPoints[i]["z"] = z

    print(allPoints)
    return(allPoints)

def __savefile(data):
    # a functin for simply saving files
    with open(f'{ROOT_DIR}/../data/arduino_data.csv', "w+", newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(data)


# on.start_level
#   1. read_serial ()
#       1.1 parseData ()
#   2. dataProcessing --> GenerateXYZ()
#   3. repackageCartesian()
#   4. updateCartesianValues()
# emit updateCartesianValues retval