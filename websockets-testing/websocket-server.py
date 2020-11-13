import asyncio
import websockets
from json import dumps
from threading import Thread
from time import sleep

command_queue = []

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = 0

    def start_server(self):
        self.server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def handler(self, ws, path):
        while True:
            if len(command_queue) > 0:
                await ws.send(command_queue[0])
                print("sent command")
                command_queue.remove(command_queue[0])
            else:
                await asyncio.sleep(1)
                broadcast_as_json({"type": "status_update",
                                        "status": "Server running"})


def broadcast_dict( target, content):
    broadcast_as_json({
        "target": target,
        "content": content
    })


def broadcast_as_json(dict_to_broadcast):
    command_queue.append(dumps(dict_to_broadcast))



ws_server = WebSocketServer("localhost", 5001)

def run_server():
    global ws_server

    ws_server.start_server()


server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

broadcast_dict("this is the target", "this is the content")

sleep(10)

broadcast_dict("this is the target", "this is the content")
print("got here")