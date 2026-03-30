#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
from websockets.asyncio.client import connect
message =[]

async def hello():
    async with connect("ws://localhost:4443") as websocket:
        message.append(await websocket.recv())
        print(message)
while True:
       asyncio.run(hello())


