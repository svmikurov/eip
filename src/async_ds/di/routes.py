"""Route table — отдельный модуль.

Чтобы избежать циклических импортов.
"""

from aiohttp import web

routes = web.RouteTableDef()
