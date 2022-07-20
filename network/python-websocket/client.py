import websockets
import asyncio

async def listen():
    url = "ws://127.0.0.1:5000"

    async with websockets.connect(url) as ws:
        await ws.send("This is python client. Connected to server " + url)
        while True:
            msg = await ws.recv()
            print(msg)
            # print(str(msg))

asyncio.get_event_loop().run_until_complete(listen())
