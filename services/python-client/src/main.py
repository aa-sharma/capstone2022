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
            #await ws.send(json.dumps({"position": "pinkyA", "x": "7", "y": "0", "z": "3"}))
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


