import serial as serial
import csv
from datetime import datetime
# from utils.helper_functions import ROOT_DIR
import logging
# from utils.config import config
import re
import serial
import math
import numpy
import time

def GenerateXYZ(angles):
    """
    Args: Angles array containing 8 elements corresponding to angles retrived from sensor.
    angles[0] -> index angle
    angles[1] -> middle angle
    angles[2] -> ring angle
    angles[3] -> pinky angle
    angles[4] -> thumb angle
    angles[5] -> roll angle
    angles[6] -> pitch angle
    angles[7] -> yaw angle

    Returns: allPoints = [X, Y, Z] An array of 3 arrays. Each of the three nested arrays have 4 elements corresponding to the 4 1-D points of a finger.
             Ex.  allPoints[0][0][0] --> The 0th dimension (x), the 0th finger (index), the 0th point (Point A)
    X = [Xpalm, Xindex, Xmiddle, Xring, Xpinky, Xthumb]
    Y = [Ypalm, Yindex, Ymiddle, Yring, Ypinky, Ythumb]
    Z = [Zpalm, Zindex, Zmiddle, Zring, Zpinky, Zthumb]
    """
    print("\nin generateXYZ()...")
    print(angles)
    t_index = angles[0]
    t_middle = angles[1]
    t_ring = angles[2]
    t_pinky = angles[3]
    t_thumb = angles[4]
    roll = angles[5]
    pitch = angles[6]
    yaw = angles[7]

    Xpalm = 0
    Ypalm = 0
    Zpalm = 0
    
    Xthumb = [0, 0, 0, 0]
    Ythumb = [0, 0, 0, 0]
    Zthumb = [0, 0, 0, 0]
    Xpinky = [0, 0, 0, 0]
    Ypinky = [0, 0, 0, 0]
    Zpinky = [0, 0, 0, 0]
    Xring = [0, 0, 0, 0]
    Yring = [0, 0, 0, 0]
    Zring = [0, 0, 0, 0]
    Xmiddle = [0, 0, 0, 0]
    Ymiddle = [0, 0, 0, 0]
    Zmiddle = [0, 0, 0, 0]
    Xindex = [0, 0, 0, 0]
    Yindex = [0, 0, 0, 0]
    Zindex = [0, 0, 0, 0]

    #Thumb position
    l = [3.5, 2]
    Q_thumb = Qtrpy(6, -1.5, 0, roll, pitch, yaw)
    Xthumb[0] = Q_thumb[0, 3]
    Ythumb[0] = Q_thumb[1, 3]
    Zthumb[0] = Q_thumb[2, 3]
    Q_thumb = numpy.dot(Q_thumb, Qtrpy(4.5*math.cos(math.pi/4), 4.5*math.sin(math.pi/4), 0, 0, 0, 0))
    Xthumb[1] = Q_thumb[0, 3]
    Ythumb[1] = Q_thumb[1, 3]
    Zthumb[1] = Q_thumb[2, 3]
    for i in range(2):
        Q_thumb = numpy.dot(Q_thumb, DenHart(l[i], t_thumb))
        Xthumb[i+2] = Q_thumb[0, 3]
        Ythumb[i+2] = Q_thumb[1, 3]
        Zthumb[i+2] = Q_thumb[2, 3]

    #Pinky position
    l = [3.5, 2, 2]
    Q_pinky = Qtrpy(0, 7, 0, 90, 0, -90)
    Xpinky[0] = Q_pinky[0, 3]
    Ypinky[0] = Q_pinky[1, 3]
    Zpinky[0] = Q_pinky[2, 3]
    for i in range(3):
        Q_pinky = numpy.dot(Q_pinky, DenHart(l[i], t_pinky))
        Xpinky[i+1] = Q_pinky[0, 3]
        Ypinky[i+1] = Q_pinky[1, 3]
        Zpinky[i+1] = Q_pinky[2, 3]
    
    #Ring position
    l = [4, 3.5, 2]
    Q_ring = Qtrpy(2, 7.5, 0, 90, 0, -90)
    Xring[0] = Q_ring[0, 3]
    Yring[0] = Q_ring[1, 3]
    Zring[0] = Q_ring[2, 3]
    for i in range(3):
        Q_ring = numpy.dot(Q_ring, DenHart(l[i], t_ring))
        Xring[i+1] = Q_ring[0, 3]
        Yring[i+1] = Q_ring[1, 3]
        Zring[i+1] = Q_ring[2, 3]
    
    #Middle position
    l = [5, 3, 2]
    Q_middle = Qtrpy(4, 7.5, 0, 90, 0, -90)
    Xmiddle[0] = Q_middle[0, 3]
    Ymiddle[0] = Q_middle[1, 3]
    Zmiddle[0] = Q_middle[2, 3]
    for i in range(3):
        Q_middle = numpy.dot(Q_middle, DenHart(l[i], t_middle))
        Xmiddle[i+1] = Q_middle[0, 3]
        Ymiddle[i+1] = Q_middle[1, 3]
        Zmiddle[i+1] = Q_middle[2, 3]
    
    #Index position
    l = [4, 3, 2]
    Q_index = Qtrpy(6, 7.5, 0, 90, 0, -90)
    Xindex[0] = Q_index[0, 3]
    Yindex[0] = Q_index[1, 3]
    Zindex[0] = Q_index[2, 3]
    for i in range(3):
        Q_index = numpy.dot(Q_index, DenHart(l[i], t_index))
        Xindex[i+1] = Q_index[0, 3]
        Yindex[i+1] = Q_index[1, 3]
        Zindex[i+1] = Q_index[2, 3]
    
    X = [Xpalm, Xindex, Xmiddle, Xring, Xpinky, Xthumb]
    Y = [Ypalm, Yindex, Ymiddle, Yring, Ypinky, Ythumb]
    Z = [Zpalm, Zindex, Zmiddle, Zring, Zpinky, Zthumb]

    return [X, Y, Z]

def Qtrpy(xT, yT, zT, roll, pitch, yaw):
    roll = math.radians(roll)
    pitch = math.radians(pitch)
    yaw = math.radians(yaw)
    A_t = [[1, 0, 0, xT],[0, 1, 0, yT],[0, 0, 1, zT],[0, 0, 0, 1]]
    A_roll = [[math.cos(roll), -math.sin(roll), 0, 0],[math.sin(roll), math.cos(roll), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    A_pitch = [[math.cos(pitch), 0, math.sin(pitch), 0], [0, 1, 0, 0], [-math.sin(pitch), 0, math.cos(pitch), 0], [0, 0, 0, 1]]
    A_yaw = [[1, 0, 0, 0], [0, math.cos(yaw), -math.sin(yaw), 0], [0, math.sin(yaw), math.cos(yaw), 0], [0, 0, 0, 1]]
    Q = numpy.dot(A_t, A_roll)
    Q = numpy.dot(Q, A_pitch)
    Q = numpy.dot(Q, A_yaw)
    return Q

def DenHart(l, theta):
    theta = math.radians(theta)
    return [[math.cos(theta), -math.sin(theta), 0,  l*math.cos(theta)],
            [math.sin(theta), math.cos(theta),  0,  l*math.sin(theta)],
            [0,               0,                1,  0],
            [0,               0,                0,  1]]



logger = logging.getLogger('logger')

# ser = serial.Serial(config.COM_PORT, config.BAUD_RATE)

def read_serial():
    print("\nin read_serial()...")

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
        # Aashna DEBUGGING
        # ser = serial.Serial('/dev/tty.usbmodem1301', 9600, timeout = 1)
        test_string = "b'168/171/175/155/175/0/0/0\r\n'"
        input = test_string
        anglesList = (parseData(input))

        # logger.debug(anglesList[x])

    return(anglesList)

def parseData(inputString):
    """
    Function to extract just the angles data from received string from serial port.
    Args: inputString of format: "b'168/171/175/155/175/0/0/0\r\n'" 
          corresponding to angles in order: index, middle, ring, pinky, thumb, roll, pitch, yaw
    Returns: anglesList appended with 8 elements corresponding to the extracted angle values
                        Ex. ['168', '171', '175', '155', '175', '0', '0', '0']
    """
    print("\nin parseData()...")
    adc = re.search("'(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)", str(inputString))
    anglesList = []
    if adc:
        for i in range(1, 9):
            anglesList.append(int(adc.group(i)))
    else:
        print(["[ERROR]: Could not parse input data."])

    return(anglesList)

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
    print("\nin repackageCartesian()...")

    # Inital
    XYZDict = {
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
        22 : {"x": "1", "y": "6", "z": "1"},
        23 : {"x": "1", "y": "6", "z": "1"}
    }

    ############ Unpack Array ############

    X = XYZ[0]
    Y = XYZ [1]
    Z = XYZ[2]

    # print(f"X: {X}\nY: {Y}\nZ: {Z}")

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
        # print("\nNext finger")
        for i in range(4):
            XYZDict[k]["x"] = X[j][i]
            XYZDict[k]["y"] = Y[j][i]
            XYZDict[k]["z"] = Z[j][i]
            
            # print(f"\nk= {k}")
            # print(f"j= {j}")
            # print(f"i= {i}")

            # print(X[j][i])
            # print(Y[j][i])
            # print(Z[j][i])
            k = k+1

    # print(f"XYZDict: {XYZDict}")
    return(XYZDict)


if __name__ == "__main__":
    anglesList = read_serial()
    print(f"anglesList: {anglesList}")
    xyz = GenerateXYZ(anglesList)
    print(f"xyz: {xyz}")
    xyz_dict = repackageCartesian(xyz)
    print(f"xyz_dict: {xyz_dict}")



# on.start_level
#   1. read_serial ()
#       1.1 parseData ()
#   2. dataProcessing --> GenerateXYZ()
#   3. repackageCartesian()
#   4. updateCartesianValues()
# emit updateCartesianValues retval



























# import re

# XYZ = [[0, 
# [6.0, 6.0, 6.0, 6.0], 
# [4.0, 4.0, 4.0, 4.0], 
# [2.0, 2.0, 1.9999999999999998, 1.9999999999999996], 
# [0.0, 4.741288034194162e-17, -3.1214284202626125e-17, -1.8552878335587686e-16], 
# [6.0, 6.415913541894264, 7.193111369252568, 6.445377145606801]
# ], 

# [0, 
# [7.5, 10.854682271781696, 12.074892201009096, 11.762023270928633], 
# [7.5, 11.64518786277521, 12.769007643022945, 12.353184261387426], 
# [7.5, 10.776608177155968, 11.973678678795808, 11.456040588590767], 
# [7.0, 9.831559480312317, 10.449593469062211, 9.831559480312317], 
# [-1.5, 2.9516335273546606, 6.319575221004481, 8.17092948265222]
# ], 

# [0, 
# [0.0, -2.1785561400601083, -4.919192512987911, -6.894569194178186], 
# [0.0, -2.7959645173537346, -5.577516081054098, -7.533811282521709], 
# [0.0, -2.294305745404184, -5.5832299181548635, -7.515081570733], 
# [0.0, -2.057248383023656, -3.959361415613963, -5.86147444820427], 
# [0.0, -0.5098773026923992, -1.0602701490528097, -0.944594184965118]
# ]
# ]

# def repackageCartesian(XYZ):
#     """
#     Args: Array of 3 subarrays with 6 sub-subarrays each corresponding to fingers/palm. 
#     Each of these 6 sub-subarrays has 4 elements for 4 points (A,B,C,D):
#     [
#         X = [Xpalm, Xindex, Xmiddle, Xring, Xpinky, Xthumb]
#         Y = [Ypalm, Yindex, Ymiddle, Yring, Ypinky, Ythumb]
#         Z = [Zpalm, Zindex, Zmiddle, Zring, Zpinky, Zthumb]
#     ]
#     Returns: Dictionary with points as the keys and x,y,z as the values
#     Map to keep track of idx and associated data point ex. pinkyA
#     +----------+----------------------+
#     | Index    |      Point Map       |
#     +----------+----------------------+
#     |    0     |        palm A       |
#     |    1     |        palm B       |
#     |    2     |        palm C       |
#     |    3     |        palm D       |
#     |    4     |        index A      |
#     |    5     |        index B      |
#     |    6     |        index C      |
#     |    7     |        index D      |
#     |    8     |        middle A     |
#     |    9     |        middle B     |
#     |    10    |        middle C     |
#     |    11    |        middle D     |
#     |    12    |        ring A       |
#     |    13    |        ring B       |
#     |    14    |        ring C       |
#     |    15    |        ring D       |
#     |    16    |        pinky A      |
#     |    17    |        pinky B      |
#     |    18    |        pinky C      |
#     |    19    |        pinky D      |
#     |    20    |        thumb A      |
#     |    21    |        thumb B      |
#     |    22    |        thumb C      |
#     |    23    |        thumb D      |
#     +----------+----------------------+
#     This function is to get the data into a format that is comprehensible to the web client. x,y,z for each point needs to be concatenated.
#     Called after the angle to xyz conversion.
#     """
#     ############ Unpack Array ############
    
#     # Ex:
#     # xindexA_direct = X[1][0]
#     # yindexA_direct = Y[1][0]
#     # zindexA_direct = Z[1][0]
#     # xindexB_direct = X[1][1]
#     # yindexB_direct = Y[1][1]
#     # zindexB_direct = Z[1][1]

#     XYZDict = {
#         0 : {"x": "7", "y": "0", "z": "3"},
#         1 : {"x": "3", "y": "2", "z": "9"},
#         2 : {"x": "8", "y": "8", "z": "8"},
#         3 : {"x": "1", "y": "6", "z": "1"},
#         4 : {"x": "1", "y": "6", "z": "1"},
#         5 : {"x": "1", "y": "6", "z": "1"},
#         6 : {"x": "7", "y": "0", "z": "3"},
#         7 : {"x": "3", "y": "2", "z": "9"},
#         8 : {"x": "8", "y": "8", "z": "8"},
#         9 : {"x": "1", "y": "6", "z": "1"},
#         10 : {"x": "1", "y": "6", "z": "1"},
#         11 : {"x": "1", "y": "6", "z": "1"},
#         12 : {"x": "8", "y": "8", "z": "8"},
#         13 : {"x": "1", "y": "6", "z": "1"},
#         14 : {"x": "1", "y": "6", "z": "1"},
#         15 : {"x": "1", "y": "6", "z": "1"},
#         16 : {"x": "7", "y": "0", "z": "3"},
#         17 : {"x": "3", "y": "2", "z": "9"},
#         18 : {"x": "8", "y": "8", "z": "8"},
#         19 : {"x": "1", "y": "6", "z": "1"},
#         20 : {"x": "1", "y": "6", "z": "1"},
#         21 : {"x": "1", "y": "6", "z": "1"},
#         22 : {"x": "1", "y": "6", "z": "1"},
#         23 : {"x": "1", "y": "6", "z": "1"}
#     }

#     X = XYZ[0]
#     Y = XYZ [1]
#     Z = XYZ[2]

#     print(f"X: {X}\nY: {Y}\nZ: {Z}")

#     # [TODO] Palm (RPY) [PARKED] HW IMPLEMENTATION IN PROGRESS
#     X[0] = [0, 0, 0, 0]    # temporarily
#     Y[0] = [0, 0, 0, 0]    # temporarily
#     Z[0] = [0, 0, 0, 0]    # temporarily

#     # k 
#     # 24 points in dictionary
#         # j
#         # 0 --> Palm
#         # 1 --> Index
#         # 2 --> Middle
#         # 3 --> Ring
#         # 4 --> Pinky
#         # 5 --> Thumb
#             # i
#             # 0 --> Point A
#             # 1 --> Point B
#             # 2 --> Point C
#             # 3 --> Point D

#     k = 0
#     for j in range(6):
#         print("\nNext finger")
#         for i in range(4):
#             XYZDict[k]["x"] = X[j][i]
#             XYZDict[k]["y"] = Y[j][i]
#             XYZDict[k]["z"] = Z[j][i]
            
#             print(f"\nk= {k}")
#             print(f"j= {j}")
#             print(f"i= {i}")

#             print(X[j][i])
#             print(Y[j][i])
#             print(Z[j][i])
#             k = k+1

#     print(f"XYZDict: {XYZDict}")
#     return(XYZDict)


# def parseData(inputString):
#     """
#     Function to extract just the angles data from received string from serial port.
#     Args: inputString of format: "b'168/171/175/155/175/0/0/0\r\n'" 
#           corresponding to angles in order: index, middle, ring, pinky, thumb, roll, pitch, yaw
#     Returns: anglesList appended with 8 elements corresponding to the extracted angle values
#                         Ex. ['168', '171', '175', '155', '175', '0', '0', '0']
#     """
#     print(str(inputString))
#     adc = re.search("'(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)\/(\+|-?\d+)", str(inputString))
#     anglesList = []
#     if adc:
#         for i in range(1, 8):
#             anglesList.append(int(adc.group(i)))
#     else:
#         print(["[ERROR]: Could not parse input data."])
#     print(anglesList)
#     return(anglesList)

# parseData("b'168/-171/175/-155/175/0/0/0\r\n'")
# # repackageCartesian(XYZ)
