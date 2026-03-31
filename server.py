"this is a cansat telemetry simulation program designed to simulate how a cansat sends data, to the ground station for visualization and storage. It is used to unders\tand how to visualize and store data properly"
import time
import json
import asyncio
import websockets
from random import uniform as aligned

""" i created 
1. an empty variable called telemetry which is a collections/set datatype. It is used to store the environmental variables and values,  
2. a variable called PORT which stores the port number where data will be transmitted from
3. a variable called interval which represensts the time interval between integer which represents the sccess
"""
PORT = 4443
telemetry = {}
interval = 1/50
telemetry = {"altitude": 0}

""" i created a sensor_simulation function to try and simulate data delivery from the cansat to the ground station"""
def sensor_simulator():
    telemetry["pressure"] = round(aligned(20, 30), 2)
    telemetry["humidity"] = round(aligned(20, 30), 2)  
    telemetry["temperature"] = round(aligned(20, 30), 2)
    telemetry["altitude"] +=0.4 
    return telemetry
        
""" i created an asynchronous data streaming function to broadcast data telemetry data from from the server"""

async def stream_data(websocket):
    while telemetry["altitude"] < 1000:
        data = sensor_simulator()
        try:
            await websocket.send(json.dumps(data))
        except websockets:exceptions.ConnectionClosedOK:


        await asyncio.sleep(0.02)  # 50 Hz

"""i created the asynchronous main function to start the asynchronous web server and end it """
async def main():
    async with websockets.serve(stream_data, "0.0.0.0", 4443) as server:
        await server.serve_forever()
try:
    print("asynchronous server running on port", PORT)
    asyncio.run(main())
except KeyboardInterrupt or websockets.exceptions.ConnectionClosedOk:
    print("Client disconnected")

