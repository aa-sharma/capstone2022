from utils.helper_functions import ROOT_DIR
from utils.logging import setup_logger
import asyncio
import websockets
from data_collection.data_collection import read_serial
from utils.config import config
from datetime import datetime
import json
import logging

logger = logging.getLogger('logger')
setup_logger()


async def listen():
    url = "ws://127.0.0.1:5000"

    async with websockets.connect(url) as ws:
        await ws.send("This is python client. Connected to server " + url)
        while True:
            data = read_serial()
            # await ws.send(json.dumps({"position": "pinkyA", "x": "7", "y": "0", "z": "3"}))
            await ws.send(json.dumps(updateValues()))

            print(str(datetime.now()) + ": [PYTHON-CLIENT INFO] Sleeping for 10 seconds")
            time.sleep(10)
            reponse = await ws.recv()
            print(reponse)
            # print(str(reponse))

if __name__ == "__main__":
    logger.info("Starting Data Processor")

    asyncio.get_event_loop().run_until_complete(listen())
    processed_data = data_processor(data)


# user sends exercise through websockets
# LOOP {
    # read angles from arduino
    # parse values into object:
    # {
    # pinkyAngle,
    # ringAngle
    # middleAngle
    # indexAngle
    # thumbAngle
    # roll,
    # pitch,
    # yaw
    # }
    # websocket computeXYZCoordinates()
    # compare parsed data with exercise['position'][0] until compare(exercise['position'][0], parsedData)
# }

# send websocket message saying they have reached the starting position
# count down from 3 to start level
# start timer for agility score
# LOOP {
    # read angles from arduino
    # parse values into object:
    # {
    # pinkyAngle,
    # ringAngle
    # middleAngle
    # indexAngle
    # thumbAngle
    # roll,
    # pitch,
    # yaw
    # }
    # websocket computeXYZCoordinates()
    # storeBestScore(exercise['position'][1], parsedData)
    # compare parsed data with exercise['position'][1] until compare(exercise['position'][1], parsedData)
# }
#
# if compare(exercise['position'][1], parsedData) {
    # stop timer
    # agilityScore = 10 - (10/500 * timeTaken)
    # dexterity = 10
# } elseif (user click interrupt button) {
    # stop timer
    # compute agility score = 10/500 * timeTaken
    # dexterityScore = bestScore
# }
# token = POST /api/auth/device ['token']
# POST /api/user-level-progress, headers = { 'x-auth-token': token }, data = {
    # exercise,
    # dexterityScore,
    # agilityScore
# }

# def storeBestScore(expectedPosition, parsedData) {
    # global bestScore
    # newScore = (10 - [(|realPinkyAngle - expectedPinkyAngle| + ... + 0.25|realYaw - expectedYaw|
    # + 0.25|realThumbAngle - expectedThumbAngle|) / 8 * 10/(90-2)
    # if newScore > bestScore {
    # bestScore = newScore
    # }
#
# }
#
# def compare (expectedPosition, parsedData) {
    # return (|realPinkyAngle - expectedPinkyAngle| + ... + 0.25|realYaw - expectedYaw|
    # + 0.25|realThumbAngle - expectedThumbAngle|) / 8 < 2
# }
