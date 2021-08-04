# aiohttpdemo_polls/views.py
from aiohttp import web
import db

import aiohttp_jinja2

@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        print(questions)
        # return web.Response(text=str(questions))
        return {"questions": questions}