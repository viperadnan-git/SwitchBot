from aiohttp import web

class ApiWebSocketView(web.View):
    async def get(self):
        key = self.request.match_info["key"]