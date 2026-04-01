import asyncio
import datetime

async def display_date():
    x = 0
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while x < 1000:
        print(datetime.datetime.now(), x)
        x+=0.1
        #if (loop.time() + 1.0) >= end_time:
         #   break
        await asyncio.sleep(0.02)

asyncio.run(display_date())
