import websockets
import asyncio
import json
import time
from datetime import datetime


def updateValues():
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
    """

    # Initial coordinates
    allPoints = {
        1: {"x": "7", "y": "0", "z": "3"},
        2: {"x": "3", "y": "2", "z": "9"},
        3: {"x": "8", "y": "8", "z": "8"},
        4: {"x": "1", "y": "6", "z": "1"},
        5: {"x": "1", "y": "6", "z": "1"},
        6: {"x": "1", "y": "6", "z": "1"},
        7: {"x": "7", "y": "0", "z": "3"},
        8: {"x": "3", "y": "2", "z": "9"},
        9: {"x": "8", "y": "8", "z": "8"},
        10: {"x": "1", "y": "6", "z": "1"},
        11: {"x": "1", "y": "6", "z": "1"},
        12: {"x": "1", "y": "6", "z": "1"},
        13: {"x": "8", "y": "8", "z": "8"},
        14: {"x": "1", "y": "6", "z": "1"},
        15: {"x": "1", "y": "6", "z": "1"},
        16: {"x": "1", "y": "6", "z": "1"},
        17: {"x": "7", "y": "0", "z": "3"},
        18: {"x": "3", "y": "2", "z": "9"},
        19: {"x": "8", "y": "8", "z": "8"},
        20: {"x": "1", "y": "6", "z": "1"},
        21: {"x": "1", "y": "6", "z": "1"},
        22: {"x": "1", "y": "6", "z": "1"},
        23: {"x": "1", "y": "6", "z": "1"}
    }

    for i in range(2):
        dataPoint = int(input("Data point: "))
        x = int(input("targetX: "))
        y = int(input("targetY: "))
        z = int(input("targetZ: "))

        allPoints[dataPoint]["x"] = x
        allPoints[dataPoint]["y"] = y
        allPoints[dataPoint]["z"] = z

    accelX = int(input("accelaration x: "))
    accelY = int(input("accelaration y: "))
    accelZ = int(input("accelaration z: "))

    allPoints[23]["x"] = accelX
    allPoints[23]["y"] = accelY
    allPoints[23]["z"] = accelZ

    print(allPoints)
    return (allPoints)


async def listen():
    url = "ws://127.0.0.1:5002"

    async with websockets.connect(url) as ws:
        await ws.send("This is python client. Connected to server " + url)
        # await ws.send(json.dumps({"position": "pinkyA", "x": "7", "y": "0", "z": "3"}))
        await ws.send(json.dumps(updateValues()))

        print(str(datetime.now()) + ": [PYTHON-CLIENT INFO] Sleeping for 10 seconds")
        time.sleep(10)
        reponse = await ws.recv()
        print(reponse)
        # print(str(reponse))

asyncio.get_event_loop().run_until_complete(listen())
