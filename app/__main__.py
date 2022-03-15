from aiohttp import web
from app import HOST, PORT
from app.views.middlewares import middleware_factory
import aiohttp_jinja2
import jinja2
from app.views.api import ApiView
from app.views.websocket import WebSocketView


async def testhandle(request):
    return web.Response(text='test handle')


async def controlhandle(request: web.Request):
    return aiohttp_jinja2.render_template("control.html", request, {})


app = web.Application(middlewares=middleware_factory())
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('public/'))
                     
app.router.add_route('GET', '/', testhandle)
app.router.add_route('GET', '/control-panel', controlhandle)
app.router.add_view('/api/{key}', ApiView)
app.router.add_view('/ws/{key}', WebSocketView)
app.router.add_static('/static', "public/static")
web.run_app(app, host=HOST, port=PORT)