"""
Tried to write unittests, but unfortunately I didn't made it in time because I didn't fully understand how to make those
"""
import unittest
from rss_reader.rss_reader import Item


class NewsFeedTest(unittest.TestCase):

    def setUp(self):
        self.item = Item({'title': 'Title', 'pubDate': 'Sun, 1 Dec 2019 20:59:28 +0300',
         'link': 'somenews.com/1.html', 'description':
             ' [link 1 |  [image 1 | Islam] ] An Irish citizen aligned to Islamic State deported from Turkey alo',
         'links': {'images_links': ['[1]: http://aee04'],
                   'href_links':['[1]: https://news.yahoo.html'], 'video_links': []},
         'date_string': '20191201', 'source': 'https://news.yahoo.com/rss', 'encoding': 'utf-8'})

    def test_return_item_true(self):

        self.assertEqual(self.item.return_item(1), {'title': 'Title',
                                                    'description': ' [link 1 |  [image 1 | Islam] ] An Irish citizen aligned to Islamic State deported from Turkey alo',
                                                    'link': 'somenews.com/1.html',
                                                    'pubDate': 'Sun, 1 Dec 2019 20:59:28 +0300',
                                                    'links': {'images_links': ['[1]: http://aee04'],
                                                              'href_links': ['[1]: https://news.yahoo.html'],
                                                              'video_links': []}, 'date_string': '20191201',
                                                    'source': 'https://news.yahoo.com/rss', 'encoding': 'utf-8'})

    def test_return_item_false(self):
        self.assertEqual(self.item.return_item(0), {'title': 'Title',
                                                    'description': ' [link 1 |  [image 1 | Islam] ] An Irish citizen aligned to Islamic State deported from Turkey alo',
                                                    'link': 'somenews.com/1.html',
                                                    'pubDate': 'Sun, 1 Dec 2019 20:59:28 +0300',
                                                    'links': {'images_links': ['[1]: http://aee04'],
                                                              'href_links': ['[1]: https://news.yahoo.html'],
                                                              'video_links': []}})

    def test_insert_images(self):

        self.assertEqual(self.item.insert_images(self.item.description, None),
              ' [link 1 | <img src="http://aee04" alt="Islam" align = "left"> ] An Irish citizen aligned to Islamic State deported from Turkey alo')

    def test_insert_hrefs(self):
        self.assertEqual(self.item.insert_hrefs(self.item.description, None),'<a href="https://news.yahoo.html"><img src="http://aee04" alt="Islam" align = "left"> </a> An Irish citizen aligned to Islamic State deported from Turkey alo')


if __name__ == '__main__':
    unittest.main()
