from tkinter import Y
import websockets
import asyncio
import json
import time
from datetime import datetime
import serial
import re

def parseData(inputData):
    """
    Function to extract just the adc data from received string from serial port.
    """
    print(str(inputData))
    adc = re.search("(\d+)", str(inputData))
    if adc:
        return adc.group(1)
    else:
        print(["[ERROR]: Could not parse input data."])

def readSerialPort():
    """
    Reading from Arduino serial port.
    5 Values are appended to anglesList (index 0-4)
        anglesList[0] -> Pinky adc
        anglesList[1] -> Ring adc
        anglesList[2] -> Middle adc
        anglesList[3] -> Index adc
        anglesList[4] -> Thumb adc
    [TODO]: This list is then passed to convertAdcToAngle()
    """
    adcDict = {
        0 : {"ADC": "7", "Angle" : "0"},
        1 : {"ADC": "7", "Angle" : "0"},
        2 : {"ADC": "7", "Angle" : "0"},
        3 : {"ADC": "7", "Angle" : "0"},
        4 : {"ADC": "7", "Angle" : "0"},
    }  
    for x in range(5):
        ser = serial.Serial('/dev/tty.usbmodem1301', 9600, timeout = 1)
        input = ser.readline()
        # print(input)

        ser.close()

        adcDict[x]["ADC"] = parseData(input)

    return(convertAdcToAngle(adcDict))
    # updateCartesianValues(anglesList)

def convertAdcToAngle(adcDict):
    """
    Mapping function to convert ADC to angles
    """
    ###################
    #### DO SOME STUFF
    ###################
    for x in range(5):
        # Change this logic. Just for demo purpose:
        adcDict[x]["Angle"] = adcDict[x]["ADC"]

    return(updateCartesianValues(adcDict))

def updateCartesianValues(adcDict):
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
        x = adcDict[i]["ADC"]
        y = adcDict[i]["ADC"]
        z = adcDict[i]["ADC"]

        allPoints[i]["x"] = x
        allPoints[i]["y"] = y
        allPoints[i]["z"] = z

    print(allPoints)
    return(allPoints)



async def listen():
    url = "ws://127.0.0.1:5050"

    async with websockets.connect(url) as ws:
        await ws.send("ID: Python Client. Connected to server " + url)
        while True:
            data = readSerialPort()
            await ws.send(json.dumps(data))

            print(str(datetime.now()) + ": [PYTHON-CLIENT INFO] Sleeping for 3 seconds\n")
            time.sleep(3)
            reponse = await ws.recv()
            print(reponse)
            # print(str(reponse))

asyncio.get_event_loop().run_until_complete(listen())
