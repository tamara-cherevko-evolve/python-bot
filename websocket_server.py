import asyncio
import json
import websockets
from constants import *
from binance.client import Client

from orders import start_listening_orders 
client = Client(api_key, api_secret) 

async def notify_client_of_filled_orders(websocket):
    while True:
        all_orders_details = start_listening_orders(client) 
        if all_orders_details:
            await websocket.send(json.dumps(all_orders_details))
        await asyncio.sleep(15)  # Check every 15 seconds


async def echo(websocket, path):
    consumer_task = asyncio.ensure_future(
        notify_client_of_filled_orders(websocket)
    )
    producer_task = asyncio.ensure_future(
        websocket.recv()
    )
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()