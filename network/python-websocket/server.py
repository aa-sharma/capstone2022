import websockets
import asyncio
from datetime import datetime

PORT = 5000

print(str(datetime.now()) + ": [INFO] Starting python websocket server on port " + str(PORT))

connected = set()

async def echo(websocket, path):
    print(str(datetime.now()) + ": [INFO] Client connection established")
    connected.add(websocket)

    try:
        async for message in websocket:
            print(str(datetime.now()) + ": [INFO] Message received from client. " + message)
            # broadcast message to all clients except the sender client
            for conn in connected:
                if conn != websocket:
                    await conn.send("Message received from server: " + message)
    except websockets.exceptions.ConnectionClosed as e:
        print(str(datetime.now()) + ": [DEBUG] A client just disconncted. Printing error message...")
        print(str(datetime.now()) + ": [ERROR] " + str(e))
    finally:
        connected.remove(websocket)

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()