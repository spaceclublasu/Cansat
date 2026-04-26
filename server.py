import time
import json
import asyncio
import websockets
from random import randint as aligned

PORT = 4443
telemetry = {"altitude": 0}

async def sensor_simulator():
    telemetry["pressure"] = aligned(0, 100000)
    telemetry["humidity"] = aligned(0, 1000)
    telemetry["temperature"] = aligned(0, 20000)
    telemetry["altitude"] += 0.105
    telemetry["voltage"] = aligned(0, 5000)
    telemetry["acceleration"] = [aligned(0, 1000), aligned(0, 1000), aligned(0, 1000)]
    telemetry["GPS Lattitude"] = aligned(0, 999999)
    telemetry["GPS Longitude"] = aligned(0, 999999)
    telemetry["Gyro"] = [aligned(0, 1000), aligned(0, 1000), aligned(0, 1000)]
    telemetry["timestamp"] = time.time()
    telemetry["Luminous Intensity"] = aligned(0, 999)
    telemetry["current"] = aligned(0, 9999)
    return telemetry

async def stream_data(websocket):
    interval = 0.021
    now = time.perf_counter()
    while telemetry["altitude"] < 999.6:
        if time.perf_counter() >= now:
            data = await sensor_simulator()
            try:
                await websocket.send(json.dumps(data))
            except websockets.exceptions.ConnectionClosedOK:
                break
            finally:
                now += interval
        await asyncio.sleep(0)

# ← Only ONE main function with origins=None
async def main():
    async with websockets.serve(
        stream_data,
        "0.0.0.0",
        4443,
        origins=None
    ) as server:
        print("asynchronous server running on port", PORT)
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server shut down")