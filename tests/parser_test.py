import unittest
from datetime import datetime

from rss_reader.storage import Article
from rss_reader.feed_parser import FeedParser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = FeedParser()
        self.maxDiff = None
        self.result = None

    def test_parse_correct_rss(self):
        self.result = Article(date=datetime.strptime("Tue, 12 Nov 2019 13:46:43 -0500", "%a, %d %b %Y %H:%M:%S %z"),
                              title="Some title & ",
                              content="[image 1: Image description][1] Some article text with intersting things",
                              media={'links': ['https://some-source.net/somelink.html'],
                                     'images': [{'description': "Image description",
                                                 'source_url': "http://some-image-link-f43ed8c16284"}]},
                              link='https://www.yahoo.com/news')

        with open('rss_example_files/correct_rss.rss') as xml_eng:
            test_data = xml_eng.read()
            self.parser.parse(test_data)
        self.assertEqual(self.parser.feed['articles'][0].date, self.result.date)
        self.assertEqual(self.parser.feed['articles'][0].title, self.result.title)
        self.assertEqual(self.parser.feed['articles'][0].content, self.result.content)
        self.assertEqual(self.parser.feed['articles'][0].media, self.result.media)
        self.assertEqual(self.parser.feed['articles'][0].link, self.result.link)
        self.assertEqual(self.parser.feed['feed_name'], 'Yahoo News - Latest News & Headlines')

    def test_parse_to_json(self):
        with open('rss_example_files/correct_rss.rss') as rss_source,\
             open('rss_example_files/example_feed.json') as json_source:
            test_data = rss_source.read()
            self.parser.parse(test_data)
            self.result = json_source.read()
        self.assertEqual(self.parser.get_json_feed(limit=1), self.result)

    def test_parse_incorrect_rss(self):
        with open('rss_example_files/incorrect_rss.rss') as rss_source:
            self.result = rss_source.read()
        with self.assertRaises(SystemExit):
            self.parser.parse(self.result)


if __name__ == "__main__":
    unittest.main()
