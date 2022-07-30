from tkinter import Y
import websockets
import asyncio
import json
import time
from datetime import datetime

def updateValues():
    """
    Updates a nested dictionary of 22 entries each for a data point. 
    TODO: Create a map to keep track of numbers and associated data point ex. pinkyA
    """
    # Initial coordinates
    allPoints = {
        1 : {"x": "7", "y": "0", "z": "3"},
        2 : {"x": "3", "y": "2", "z": "9"},
        3 : {"x": "8", "y": "8", "z": "8"},
        4 : {"x": "1", "y": "6", "z": "1"}
    }
    for i in range (2):
        dataPoint = int(input("Data point: "))
        x = int(input("targetX: "))
        y = int(input("targetY: "))
        z = int(input("targetZ: "))

        allPoints[dataPoint]["x"] = x
        allPoints[dataPoint]["y"] = y
        allPoints[dataPoint]["z"] = z

    print(allPoints)
    return(allPoints)

async def listen():
    url = "ws://127.0.0.1:5000"

    async with websockets.connect(url) as ws:
        await ws.send("This is python client. Connected to server " + url)
        while True:
            #await ws.send(json.dumps({"position": "pinkyA", "x": "7", "y": "0", "z": "3"}))
            await ws.send(json.dumps(updateValues()))

            print(str(datetime.now()) + ": [PYTHON-CLIENT INFO] Sleeping for 10 seconds")
            time.sleep(10)
            reponse = await ws.recv()
            print(reponse)
            # print(str(reponse))

asyncio.get_event_loop().run_until_complete(listen())


