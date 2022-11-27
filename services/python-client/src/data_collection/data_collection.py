import serial as serial
import csv
from datetime import datetime
from utils.helper_functions import ROOT_DIR
import logging
from utils.config import config
import re
import data_processor.dataProcessor

logger = logging.getLogger('logger')


def read_serial():
    """
    Reading from Arduino serial port.
    Sample Data Example: b'168/171/175/155/175/0/0/0\r\n'
                Order: index, middle, ring, pinky, thumb, roll, pitch, yaw
    Returns: List with 8 entries of angles.
                [0] -> Index angle
                [1] -> Middle angle
                [2] -> Ring angle
                [3] -> Pinky angle
                [4] -> Thumb angle
                [5]* -> Roll
                [6]* -> Pitch
                [7]* -> Yaw
    """

    for x in range(8):
        try:
            ser = serial.Serial(config.COM_PORT, 9600, timeout=1)
            input = ser.readline()
            ser.close()
            anglesList = (parseData(input))
        except:
            # Tested using test_string only. To be tested with HW integration.
            test_string = "b'168/171/175/155/175/0/0/0\r\n'"
            input = test_string
            anglesList = (parseData(input))

        # Write to file not tested.
        logger.debug(anglesList[x])
        if config.WRITE_ARUDINO_DATA:
            __savefile(anglesList[x])

    return (anglesList)


def parseData(inputString):
    """
    Function to extract just the angles data from received string from serial port.
    Args: inputString of format: "b'168/171/175/155/175/0/0/0\r\n'" 
          corresponding to angles in order: index, middle, ring, pinky, thumb, roll, pitch, yaw
    Returns: anglesList appended with 8 elements corresponding to the extracted angle values
                        Ex. ['168', '171', '175', '155', '175', '0', '0', '0']
    """
    adc = re.search(
        "'(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)", str(inputString))
    anglesList = []
    if adc:
        for i in range(1, 9):
            anglesList.append(int(adc.group(i)))
    else:
        logger.error(["Could not parse input data."])

    return (anglesList)


def repackageCartesian(XYZ):
    """
    Args: Array of 3 subarrays with 6 sub-subarrays each corresponding to fingers/palm. 
    Each of these 6 sub-subarrays has 4 elements for 4 points (A,B,C,D):
    [
        X = [Xpalm, Xindex, Xmiddle, Xring, Xpinky, Xthumb]
        Y = [Ypalm, Yindex, Ymiddle, Yring, Ypinky, Ythumb]
        Z = [Zpalm, Zindex, Zmiddle, Zring, Zpinky, Zthumb]
    ]
            Xindex = [XindexA, XindexB, XindexC, XindexD]
    Ex:
    xindexA = X[1][0]
    yindexA = Y[1][0]
    zindexA = Z[1][0]
    xindexB = X[1][1]
    yindexB = Y[1][1]
    zindexB = Z[1][1]

    Returns: Dictionary with points as the keys and x,y,z as the values. 
    Map to indicate which key corresponds to what point.
    +----------+----------------------+
    |  Key     |      Point Map       |
    +----------+----------------------+
    |    0     |        palm A       |
    |    1     |        palm B       |
    |    2     |        palm C       |
    |    3     |        palm D       |
    |    4     |        index A      |
    |    5     |        index B      |
    |    6     |        index C      |
    |    7     |        index D      |
    |    8     |        middle A     |
    |    9     |        middle B     |
    |    10    |        middle C     |
    |    11    |        middle D     |
    |    12    |        ring A       |
    |    13    |        ring B       |
    |    14    |        ring C       |
    |    15    |        ring D       |
    |    16    |        pinky A      |
    |    17    |        pinky B      |
    |    18    |        pinky C      |
    |    19    |        pinky D      |
    |    20    |        thumb A      |
    |    21    |        thumb B      |
    |    22    |        thumb C      |
    |    23    |        thumb D      |
    +----------+----------------------+
    """
    # Inital
    XYZDict = {
        # "palmA": {"x": "7", "y": "0", "z": "3"},
        # "indexA": {"x": "3", "y": "2", "z": "9"},
        # "indexB": {"x": "8", "y": "8", "z": "8"},
        0: {"x": "8", "y": "8", "z": "8"},
        1: {"x": "8", "y": "8", "z": "8"},
        2: {"x": "8", "y": "8", "z": "8"},
        3: {"x": "8", "y": "8", "z": "8"},
        3: {"x": "1", "y": "6", "z": "1"},
        4: {"x": "1", "y": "6", "z": "1"},
        5: {"x": "1", "y": "6", "z": "1"},
        6: {"x": "7", "y": "0", "z": "3"},
        7: {"x": "3", "y": "2", "z": "9"},
        8: {"x": "8", "y": "8", "z": "8"},
        9: {"x": "1", "y": "6", "z": "1"},
        10: {"x": "1", "y": "6", "z": "1"},
        11: {"x": "1", "y": "6", "z": "1"},
        12: {"x": "8", "y": "8", "z": "8"},
        13: {"x": "1", "y": "6", "z": "1"},
        14: {"x": "1", "y": "6", "z": "1"},
        15: {"x": "1", "y": "6", "z": "1"},
        16: {"x": "7", "y": "0", "z": "3"},
        17: {"x": "3", "y": "2", "z": "9"},
        18: {"x": "8", "y": "8", "z": "8"},
        19: {"x": "1", "y": "6", "z": "1"},
        20: {"x": "1", "y": "6", "z": "1"},
        21: {"x": "1", "y": "6", "z": "1"},
        22: {"x": "1", "y": "6", "z": "1"},
        23: {"x": "1", "y": "6", "z": "1"}
    }

    # mapping = {
    #     1: "palmA",
    #     2: "indexA"
    # }

    ############ Unpack Array ############

    X = XYZ[0]
    Y = XYZ[1]
    Z = XYZ[2]

    # [TODO] Palm (RPY) [PARKED] HW IMPLEMENTATION IN PROGRESS
    X[0] = [0, 0, 0, 0]    # temporarily
    Y[0] = [0, 0, 0, 0]    # temporarily
    Z[0] = [0, 0, 0, 0]    # temporarily

    # j
    # 0 --> Palm
    # 1 --> Index
    # 2 --> Middle
    # 3 --> Ring
    # 4 --> Pinky
    # 5 --> Thumb
    # i
    # 0 --> Point A
    # 1 --> Point B
    # 2 --> Point C
    # 3 --> Point D

    k = 0
    for j in range(6):
        for i in range(4):
            # XYZDict[mapping[k]]["x"] = X[j][i]
            # XYZDict[mapping[k]]["y"] = Y[j][i]
            # XYZDict[mapping[k]]["z"] = Z[j][i]
            XYZDict[k]["x"] = X[j][i]
            XYZDict[k]["y"] = Y[j][i]
            XYZDict[k]["z"] = Z[j][i]

            k = k+1

    logger.debug(XYZDict)
    return (XYZDict)


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
