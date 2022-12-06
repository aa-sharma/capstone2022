from utils.helper_functions import ROOT_DIR
from utils.logging import setup_logger
import asyncio
# from data_collection.data_collection import read_serial
from utils.config import config
import requests
import json
import logging
from ws.websocket import sio

logger = logging.getLogger('logger')
setup_logger()


if __name__ == "__main__":

    sio.token_data = requests.post(f"{config.BASE_SERVER_URL}/api/auth/device",
                                   json={"productCode": config.PRODUCT_CODE})

    if (sio.token_data.status_code != 200):
        logger.error(f"request for token failed with message:{json.dumps(sio.token_data.json(), indent=4)}")
        exit(0)

    sio.connect(config.BASE_SERVER_URL, auth={'x-auth-token': sio.token_data.json()['token']}, transports=['websocket'])
    sio.emit('python_client_connected', {'msg': 'message from the python client'})


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
# parse values into object: { pinkyAngle, ringAngle, middleAngle, indexAngle, roll, pitch, yaw }
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
