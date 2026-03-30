import time
import json
import asyncio
import websockets
from random import uniform as aligned

PORT = 4443
telemetry = {}
interval = 1/50
telemetry = {"altitude": 0}

def sensor_simulator():
    telemetry["pressure"] = round(aligned(20, 30), 2)
    telemetry["humidity"] = round(aligned(20, 30), 2)  
    telemetry["temperature"] = round(aligned(20, 30), 2)
    telemetry["altitude"] +=20 
    return telemetry
        

async def stream_data(websocket):
    try:
        while telemetry["altitude"] < 1000:
            data = sensor_simulator()
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.02)  # 50 Hz
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(stream_data, "0.0.0.0", 4443) as server:
        await server.serve_forever()
try:
    print("asynchronous server running on port", PORT)
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n Shutting down server")
