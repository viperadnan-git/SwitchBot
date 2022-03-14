from aiohttp.web import Request
from aiohttp import web
from app.helper.validator import JSONValidator
from app import BUTTON_STATE
from app.utils import get_button_states, update_board


class ApiView(web.View):
    async def get(self):
        key = self.request.match_info['key']
        return web.json_response(get_button_states(key))

    async def post(self):
        key = self.request.match_info['key']
        try:
            body:dict = await self.request.json()
            if not JSONValidator().switch(body):
                raise ValueError("Invalid JSON provided")
        except Exception as err:
            return web.json_response({"error": str(err)})
        
        buttons_state = get_button_states(key)
        for switch, val in body.items():
            BUTTON_STATE[key][switch] = val


        status = await update_board(key, body)
        
        return web.json_response(status)