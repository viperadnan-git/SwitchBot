from aiohttp import web, WSMsgType
from aiohttp.web import Request
from app import HOST, PORT, WEBSOCKETS, BUTTON_STATE, ALL_SWITCH_OFF
from app.helper.validator import JSONValidator
from app.views.middlewares import middleware_factory
from app.utils import update_board
from app.views.api import ApiView


async def testhandle(request):
    return web.Response(text='test handle')




async def websocket_handler(request:Request):
    key = request.match_info['key']
    print('Websocket connection starting')
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')
    WEBSOCKETS[key] = ws

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            print(msg.data)
            if msg.data == "update":
                await update_board(key)
            else:
                try:
                    data:dict = msg.json()
                    if JSONValidator().switch(data):
                        for switch, value in data.items():
                            BUTTON_STATE[key][switch] = value
                except KeyError:
                    pass
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

            
    print('Websocket connection closed')
    del WEBSOCKETS[key]
    return ws


app = web.Application(middlewares=middleware_factory())
app.router.add_route('GET', '/', testhandle)
app.router.add_view('/api/{key}', ApiView)
app.router.add_route('GET', '/ws/{key}', websocket_handler)
web.run_app(app, host=HOST, port=PORT)