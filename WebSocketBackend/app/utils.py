from aiohttp import web
from app import BUTTON_STATE, ALL_SWITCH_OFF, WEBSOCKETS

def get_button_states(key: str) -> dict:
    if not BUTTON_STATE.get(key):
        BUTTON_STATE[key] = ALL_SWITCH_OFF
    return BUTTON_STATE[key]


async def update_board(key: str, data: dict = None) -> dict:
    try:
        ws: web.WebSocketResponse = WEBSOCKETS[key]
        if not data:
            data = get_button_states(key)
        try:
            await ws.send_json(data)
            return {
                "success": True,
                "data": data
            }
        except ConnectionResetError:
            return {
                "success": False,
                "data": "Board is not online"
            }
    except KeyError:
        return {
            "success": False,
            "data": "Board is not online"
        }
