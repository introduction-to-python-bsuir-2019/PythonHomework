# aiohttpdemo_polls/main.py
from routes import setup_routes
from aiohttp import web
from settings import config
from db import init_pg, close_pg

app = web.Application()
setup_routes(app)
app['config'] = config
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
web.run_app(app)