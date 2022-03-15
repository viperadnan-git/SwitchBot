from aiohttp import BasicAuth, web, hdrs
from aiohttp.web import middleware, Request

def middleware_factory():
    @middleware
    async def basic_auth(request:Request, handler):
        if request.path.startswith('/ws/') or request.path.startswith("/api/"):
            username = request.match_info['key']
            password = "00"
            auth_header = request.headers.get(hdrs.AUTHORIZATION)
            if auth_header:
                try:
                    auth = BasicAuth.decode(auth_header=auth_header)
                    if auth.login == username and auth.password == password:
                        return await handler(request)
                except ValueError:
                    pass
            return web.HTTPForbidden()
        return await handler(request)
    return [basic_auth]