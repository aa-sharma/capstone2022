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


@sio.on("user_start_exercise")
def start_exercise(data):
    logger.info(f'User requested to start exercise:\n{json.dumps(data, indent=4)}')
    sio.run_level = True

    while sio.start_level:
        pass

    while sio.run_level:
        logger.info("running")
        time.sleep(1)


@sio.event
def connect():
    logger.info(f"Successfully connected websocket server: {config.BASE_SERVER_URL}")


@sio.on('connect_error')
def connect_error(data):
    logger.warning(f"Websocket connection to {config.BASE_SERVER_URL} failed, with reason: {data}")


@sio.event
def disconnect():
    logger.info(f"Disconnected from websocket server: {config.BASE_SERVER_URL}")
