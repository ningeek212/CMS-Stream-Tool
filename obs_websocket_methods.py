import asyncio
import simpleobsws

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444)


async def async_connect():
    await ws.connect()

loop.run_until_complete(async_connect())


async def async_disconnect():
    await ws.disconnect()


async def set_map_cinematic_async(n):

    sources = ["MapVideo1", "MapVideo2", "MapVideo3"]
    count = 1
    for source in sources:
        data = {
            'scene-name': "Next Map",
            'item': source,
            'visible': count == n,
        }
        result = await ws.call('SetSceneItemProperties', data)
        if result["status"] == "ok":
            # print("Map source visibility changed successfully")
            pass
        count += 1


def set_map_cinematic(map_id):
    loop.run_until_complete(set_map_cinematic_async(map_id))


def disconnect():
    loop.run_until_complete(async_disconnect())
