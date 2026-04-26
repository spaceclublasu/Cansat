#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
from websockets.asyncio.client import connect
async def get_data():
    async with connect("ws://localhost:4443") as websocket:
       # message = await websocket.recv()
        async for message in websocket:
            print(message)
try:
    while True:
        asyncio.sleep(0.02)
        asyncio.run(get_data())
except KeyboardInterrupt:
    print("\n connection closed\n")

