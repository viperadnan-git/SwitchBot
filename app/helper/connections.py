from aiohttp import web
from app import TEMP_CON_DB
from app.helper.validator import JSONValidator

DEFAULT_BUTTON_STATE = {
    "1": False,
    "2": False,
    "3": False,
    "4": False,
    "5": False,
    "6": False,
    "7": False,
    "8": False
}


class ConnectionManager():
    def __init__(self, device_username:str, connection: web.WebSocketResponse) -> None:
        self.device_username = device_username
        self.connection = connection
        self.button_state = TEMP_CON_DB.get(device_username) or DEFAULT_BUTTON_STATE
        self.api_connections = []

    async def send_json(self, data: dict):
        await self.connection.send_json(data)

    async def send_str(self, data: str):
        await self.connection.send_str(data)

    async def update_button_state(self, data: dict):
        if JSONValidator().switch_button(data):
            for key, val in data.items():
                self.button_state[key] = val
            return True
        return False

    async def add_api_ws(self, ws: web.WebSocketResponse):
        if not ws in self.api_connections:
            self.api_connections.append(ws)

    async def del_api_ws(self, ws: web.WebSocketResponse):
        if ws in self.api_connections:
            self.api_connections.remove(ws)

    async def update_api_ws(self, data: dict):
        for ws in self.api_connections:
            ws: web.WebSocketResponse
            await ws.send_json(data=data)

    async def update_device(self, data: dict):
        if (await self.update_button_state(data=data)):
            await self.send_json(data=data)
            await self.save_button_state()
            await self.update_api_ws(data=data)
            return True
        return False
    
    async def save_button_state(self):
        TEMP_CON_DB[self.device_username] = self.button_state
