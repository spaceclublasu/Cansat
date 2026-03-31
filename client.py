#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
from websockets.asyncio.client import connect
message =[]

async def hello():
    async with connect("ws://localhost:4443") as websocket:
       # message = await websocket.recv()
        async for message in websocket:
            print(message)
try:
    while True:
       asyncio.run(hello())
except KeyboardInterrupt:
    print("\n connection closed\n")

