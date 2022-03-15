from aiohttp import web
from app import ACTIVE_DEVICES
from app.helper.connections import ConnectionManager


class ApiView(web.View):
    async def get(self):
        key = self.request.match_info['key']
        ws_manager = ACTIVE_DEVICES.get(key)
        if ws_manager:
            ws_manager: ConnectionManager
            return web.json_response(ws_manager.button_state)
        else:
            return web.json_response({})

    async def post(self):
        key = self.request.match_info['key']
        print(await self.request.text())
        ws_manager = ACTIVE_DEVICES.get(key)
        if ws_manager:
            ws_manager: ConnectionManager

            try:
                data: dict = await self.request.json()
            except Exception as err:
                return web.json_response({"error": str(err)})

            if (await ws_manager.update_device(data)):
                return web.json_response({
                    "status": True,
                    "data": data
                })
            return web.json_response({
                "status": False,
                "data": "Invalid JSON"
            })
        return web.json_response({
            "status": False,
            "data": "Device offline"
        })
