from aiohttp import web
from app.helper.connections import ConnectionManager
from aiohttp import WSMsgType
from app import ACTIVE_DEVICES

class WebSocketView(web.View):
    async def get(self):
        key = self.request.match_info['key']
        print('Websocket connection starting')
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        print('Websocket connection ready')
        ws_manager = ConnectionManager(device_username=key, connection=ws)
        ACTIVE_DEVICES[key] = ws_manager

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                print(msg.data)
                if msg.data == "update":
                    await ws_manager.update_device(ws_manager.button_state)
                else:
                    try:
                        data:dict = msg.json()
                        await ws_manager.update_button_state(data=data)
                    except KeyError:
                        pass
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())

                
        print('Websocket connection closed')
        await ws_manager.save_button_state()
        del ACTIVE_DEVICES[key]
        return ws