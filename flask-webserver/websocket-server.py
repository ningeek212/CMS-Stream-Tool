#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import websockets
from json import dumps

command_queue = []

def broadcast_dict(target, content):
    broadcast_as_json({
        "target": target,
        "content": content
    })


def broadcast_as_json(dict_to_broadcast):
    command_queue.append(dumps(dict_to_broadcast))


async def handler(ws, path):
    while True:
        if len(command_queue) > 0:
            await ws.send(command_queue[0])
            print("sent command")
            command_queue.remove(command_queue[0])
        else:
            await asyncio.sleep(1)
            broadcast_as_json({"type": "status_update",
                               "status": "Server running"})


start_server = websockets.serve(handler, "localhost", 5001)

broadcast_as_json({"test": "this is a test"})

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
