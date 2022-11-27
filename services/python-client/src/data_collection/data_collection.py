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
    |    1     |        index A      |
    |    2     |        index B      |
    |    3     |        index C      |
    |    4     |        index D      |
    |    5     |        middle A     |
    |    6     |        middle B     |
    |    7     |        middle C     |
    |    9     |        middle D     |
    |    9     |        ring A       |
    |    10    |        ring B       |
    |    11    |        ring C       |
    |    12    |        ring D       |
    |    13    |        pinky A      |
    |    14    |        pinky B      |
    |    15    |        pinky C      |
    |    16    |        pinky D      |
    |    17    |        thumb A      |
    |    18    |        thumb B      |
    |    19    |        thumb C      |
    |    20    |        thumb D      |
    +----------+----------------------+
    """
    # Inital
    XYZDict = {
        "palmA": {"x": "7", "y": "0", "z": "3"},
        "indexA": {"x": "3", "y": "2", "z": "9"},
        "indexB": {"x": "8", "y": "8", "z": "8"},
        "indexC": {"x": "8", "y": "8", "z": "8"},
        "indexD": {"x": "1", "y": "6", "z": "1"},
        "middleA": {"x": "7", "y": "0", "z": "3"},
        "middleB": {"x": "3", "y": "2", "z": "9"},
        "middleC": {"x": "8", "y": "8", "z": "8"},
        "middleD": {"x": "1", "y": "6", "z": "1"},
        "ringA": {"x": "1", "y": "6", "z": "1"},
        "ringB": {"x": "1", "y": "6", "z": "1"},
        "ringC": {"x": "8", "y": "8", "z": "8"},
        "ringD": {"x": "1", "y": "6", "z": "1"},
        "pinkyA": {"x": "1", "y": "6", "z": "1"},
        "pinkyB": {"x": "1", "y": "6", "z": "1"},
        "pinkyC": {"x": "7", "y": "0", "z": "3"},
        "pinkyD": {"x": "3", "y": "2", "z": "9"},
        "thumbA": {"x": "8", "y": "8", "z": "8"},
        "thumbB": {"x": "1", "y": "6", "z": "1"},
        "thumbC": {"x": "1", "y": "6", "z": "1"},
        "thumbD": {"x": "1", "y": "6", "z": "1"},
    }

    mapping = {
        0: "palmA",
        1: "indexA",
        2: "indexB",
        3: "indexC",
        4: "indexD",
        5: "middleA",
        6: "middleB",
        7: "middleC",
        8: "middleD",
        9: "ringA",
        10: "ringB",
        11: "ringC",
        12: "ringD",
        13: "pinkyA",
        14: "pinkyB",
        15: "pinkyC",
        16: "pinkyD",
        17: "thumbA",
        18: "thumbB",
        19: "thumbC",
        20: "thumbD"
    }

    ############ Unpack Array ############

    X = XYZ[0]
    Y = XYZ[1]
    Z = XYZ[2]

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
            if j == 0:
                XYZDict[mapping[k]]["x"] = X[j]
                XYZDict[mapping[k]]["y"] = Y[j]
                XYZDict[mapping[k]]["z"] = Z[j]
                break
            else:
                XYZDict[mapping[k]]["x"] = X[j][i]
                XYZDict[mapping[k]]["y"] = Y[j][i]
                XYZDict[mapping[k]]["z"] = Z[j][i]
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
