#!/usr/bin/env python
import json
"""Client using the asyncio API."""
interval = float(input(" specify data transmission interval e.g 1.02 means 1.02Hz "))
max_altitude = float(input("specify maximum altitude e.g 1000 means 1km"))
speed  = float(input("specify ascent speed"))

import struct
import asyncio
from websockets.asyncio.client import connect
async def get_data():
    async with connect("ws://localhost:4443") as websocket:
        # message = await websocket.recv()
        await websocket.send(json.dumps([interval, max_altitude, speed]))
        async for message in websocket:
            print(struct.unpack("< i i i i h i B H h h h h h h H H ", message))
            await asyncio.sleep(0.02)
try:
    asyncio.run(get_data())
except KeyboardInterrupt:
    print("\n connection closed\n")

