import serial
import math
import numpy
import time


##### ERIC'S ALGORITHM #####

# def parseData(inputData):
#     angles = str(inputData).split("'")
#     angles = angles[1].split("\\")
#     angles = angles[0].split("/")
#     angles = int(angles)
#     return angles

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

#ser = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout = 1)
#input = ser.readline()
#print("recieved string: " + str(input))
#ser.close()

#anglesList = parseData(input)
#print("Parsed angles")
#print("thetaindex = " + anglesList[0])
#print("thetamiddle = " + anglesList[1])
#print("thetaring = " + anglesList[2])
#print("thetapinky = " + anglesList[3])
#print("thetathumb = " + anglesList[4])
#print("roll = " + anglesList[5])
#print("pitch = " + anglesList[6])
#print("yaw = " + anglesList[7])

start = time.process_time()
XYZ = GenerateXYZ([33, 34, 35, 36, 37, 40, 18, 9])
print(XYZ)
print(time.process_time() - start)

