import socketio
import logging
import time
import json
from utils.config import config
from data_collection import data_collection
from data_processor import dataProcessor

sio = socketio.Client()
logger = logging.getLogger('logger')


@sio.on("user_stop_exercise")
def stop_exercise(data):
    logger.info(data)
    sio.run_level = False
    sio.start_level = False


@sio.on("user_start_exercise")
def start_exercise(expected_angles):
    logger.info(f'User requested to start exercise:\n{json.dumps(expected_angles, indent=4)}')
    sio.start_level = True
    sio.run_level = True

    while sio.start_level:
        # read values from Arduino
        raw_data = data_collection.read_serial()  # outputs angles dict (NEEDS TO BE ARRAY)
        raw_xyz = dataProcessor.GenerateXYZ(raw_data)
        processed_xyz = data_collection.repackageCartesian(raw_xyz)
        sio.emit('python_client_data', processed_xyz)
        time.sleep(0.1)

    # best_score = 0

    # while sio.run_level:
    #     logger.info("running")
    #     new_score = dexterity_score(expected_angles, raw_data)
    #     if new_score > best_score:
    #         best_score = new_score

    #     time.sleep(1)


@sio.event
def connect():
    logger.info(f"Successfully connected websocket server: {config.BASE_SERVER_URL}")


@sio.on('connect_error')
def connect_error(data):
    logger.warning(f"Websocket connection to {config.BASE_SERVER_URL} failed, with reason: {data}")


@sio.event
def disconnect():
    logger.info(f"Disconnected from websocket server: {config.BASE_SERVER_URL}")
