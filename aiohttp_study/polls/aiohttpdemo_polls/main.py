# aiohttpdemo_polls/main.py
from routes import setup_routes
from aiohttp import web
from settings import config

app = web.Application()
setup_routes(app)
app['config'] = config
web.run_app(app)