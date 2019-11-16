import unittest
from unittest import mock

from rss_reader.main import RSS_reader


class Args():
    def __init__(self):
        self.source = 'https://example.com'
        self.limit = 2
        self.json = True


class TestRSS_reader(unittest.TestCase):
    def setUp(self):
        self.cmd_args = Args()

    def _mock_response(self, status):
        resp = mock.Mock()
        resp.status_code = status
        if status == 200:
            resp.ok = True
            with open('rss_example_files/correct_rss.rss') as sourse:
                resp.content = sourse.read()
        else:
            resp.ok = False
            resp.content = ' '
        return resp

    @mock.patch('requests.get')
    def test_get_feed_from_source_500(self, mock_get):
        resp = self._mock_response(500)
        mock_get.return_value = resp

        reader = RSS_reader(self.cmd_args)
        with self.assertRaises(SystemExit):
            reader.get_feed_from_source()

    @mock.patch('requests.get')
    def test_get_feed_from_source_correct(self, mock_get):
        resp = self._mock_response(200)
        mock_get.return_value = resp

        reader = RSS_reader(self.cmd_args)
        reader.get_feed_from_source()
        with open('rss_example_files/example_feed.json') as source:
            self.assertEqual(reader.parser.get_json_feed(limit=1), source.read())


if __name__ == "__main__":
    unittest.main()
