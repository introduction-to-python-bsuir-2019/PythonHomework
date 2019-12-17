from webapi import app, api
from flask_restful import Resource, reqparse, inputs
import subprocess


class Index(Resource):
    def get(self):
        return 'Simply main page'


api.add_resource(Index, '/')


class News(Resource):
    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('source', type=inputs.url, location='json', required=True)
        parser.add_argument('limit', type=inputs.positive, location='json')
        parser.add_argument('date', type=inputs.date, location='json')
        self.args = parser.parse_args(strict=True)

    def get(self):
        args = ["rss-reader", self.args['source']]

        # add limit if set
        limit = self.args.get('limit')
        if limit:
            args.extend(['--limit', str(limit)])

        # load cached news if specified
        date = self.args.get('date')
        if date:
            args.extend(['--date', date.strftime('%Y%m%d')])

        result = subprocess.run(args, capture_output=True)
        return result.stdout.decode("utf-8")


api.add_resource(News, '/api/v1.0/news')


if __name__ == '__main__':
    app.run(debug=True)
