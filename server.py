"this is a cansat telemetry simulation program designed to simulate how a cansat sends data, to the g  station for visualization and storage. It is used to unders\tand how to visualize and store data properly"
CLIENT_QUEUES = set()
import time, math
import json
import asyncio
import websockets
import datetime
from struct import pack
from random import randint as aligned

""" i created 
1. an empty variable called telemetry which is a collections/set datatype. It is used to store the environmental variables and values,  
2. a variable called PORT which stores the port number where data will be transmitted from
4. a variable called interval which represensts the time interval between integer which represents the sccess
"""
PORT = 4443
count = 0
telemetry= {"altitude": 0}
frequency = float(input(" specify data transmission interval e.g 1.02 means 1.02Hz "))
interval = float(1/frequency)
max_altitude = int(input("specify maximum altitude e.g 1000 means 1km"))
speed  = float(input("specify ascent speed e.g 5 means 5m/s"))
Height_per_cycle = int(float(speed/frequency) * 1000)
start = time.time()
def sensor_simulator(Height_per_cycle):
    time.sleep(interval) 
    global count
    count += 1
    now = time.time()
    print(interval,count)
    telemetry["pressure"] = aligned(0, 100000)
    telemetry["humidity"] = aligned(0,255)  
    telemetry["temperature"] = aligned(0, 20000)
    telemetry["altitude"] += Height_per_cycle
    telemetry["voltage"] = aligned(0, 5000)
    telemetry["acceleration"] = [aligned(0, 1000), aligned(0, 1000), aligned(0, 1000)]
    telemetry["GPS Lattitude"] = aligned(0, 999999)
    telemetry["GPS Longitude"] = aligned(0, 999999)
    telemetry["Gyro"] = [aligned(0, 1000), aligned(0, 1000), aligned(0, 1000)]
    telemetry["timestamp"] =int( (now - start)*10000)
    telemetry["Lux"] =aligned(0, 999)
    telemetry["current"] =aligned(0, 9999) 
    return telemetry


""" i created an asynchronous data streaming function to broadcast data telemetry data from from the server"""
Tele_list =[sensor_simulator(Height_per_cycle).copy() for x in range(0, max_altitude) if telemetry["altitude"]/1000 < max_altitude]
print(Tele_list)
async def stream_data(websocket):
    """interval = float(1/frequency)
    queue  = asyncio.Queue()
    relay_task = asyncio.create_task(relay(queue, websocket)) 
    print(interval, max_altitude)
    now = time.perf_counter()
    while telemetry["altitude"]/1000 < max_altitude:
        await sensor_simulator(Height_per_cycle)
        next_time  = time.perf_counter()
        print("next time = ", next_time)
        if next_time >= now:""" 
    for telemetry in Tele_list:
        bin_data = pack("< i i i i h i B H h h h h h h H H ", telemetry["timestamp"],telemetry["GPS Lattitude"],telemetry["GPS Longitude"], telemetry["altitude"], telemetry["temperature"],telemetry["pressure"], telemetry["humidity"],telemetry["Lux"], telemetry["acceleration"][0], telemetry["acceleration"][1],telemetry["acceleration"][2], telemetry["Gyro"][0],telemetry["Gyro"][1], telemetry["Gyro"][2], telemetry["voltage"],telemetry["current"]) 
        try:
            print(87)
            await websocket.send(bin_data)
            #now += interval
            print(23)
            await asyncio.sleep(interval)
        except websockets.exceptions.ConnectionClosedOK:
            continue
        finally:
            #now += interval
            print(4566)
            ##finally:continue

"""i created the asynchronous main function to start the asynchronous web server and end it """
async def main():
    await asyncio.sleep(10)
    async with websockets.serve(stream_data, "0.0.0.0", 4443) as server:
        print("asynchronous server running on port", PORT)
        await server.serve_forever()
try:
    asyncio.run(main())
except KeyboardInterrupt or websockets.exceptions.ConnectionClosedOk:
    print("Client disconnected")

