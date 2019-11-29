from datetime import datetime
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from pathlib import Path
from rss_reader import rss
from rss_reader.utils.data_structures import ConsoleArgs
from rss_reader.bots import default
from rss_reader.utils.rss_utils import get_date

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html', now=datetime.now().strftime('%Y-%m-%d'))


#
#
@app.route('/v6.0/news', methods=['GET', 'POST'])
def get_news():
    logger = rss.logger_init()
    path_to_html = Path('templates/here.html')
    path_to_pdf = Path('templates/pdf.pdf')
    to_pdf = ''
    if_pdf = False
    url = ''
    date = ''
    limit = 5

    if request.method == 'POST':

        form_data = request.form
        url = form_data.get('url')
        limit = int(form_data.get('limit'))
        if_pdf = form_data.get('is_pdf', False)
        date = form_data.get('date') if form_data.get('is_date') else ''
        if date:
            date = get_date(date).strftime('%Y%m%d')

    else:
        url = request.args.get('url', 'https://news.google.com/news/rss')

    args = ConsoleArgs(
        url=url,
        limit=limit,
        to_html=path_to_html,
        to_pdf=path_to_pdf if if_pdf else '',
        date=date,
    )
    try:
        bot = default.Bot(args, logger)
    except Exception as ex:
        return str(ex)
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
