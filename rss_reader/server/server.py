from datetime import datetime
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from pathlib import Path
from rss_reader import rss
from rss_reader.utils.data_structures import ConsoleArgs
from rss_reader.bots import default

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html', now=datetime.now().strftime('%Y-%m-%d'))
#
#
@app.route('/v6.0/news', methods=['GET', 'POST'])
def get_news():

    url = request.args.get('url', 'https://news.google.com/news/rss')

    logger = rss.logger_init()
    path_to_html = Path('templates/here.html')
    args = ConsoleArgs(
        url=url,
        limit=1,
        to_html=path_to_html,
    )
    bot = default.Bot(args, logger)
    return render_template('here.html')


class News(Resource):
    def get(self, news_id):
        return {'hello': 'world'}

class NewsList(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(News, '/api/news')

if __name__ == '__main__':
    app.run(debug=True)
