import unittest
from datetime import datetime
from rss_reader.news import News


class TestNews(unittest.TestCase):
    def test_str_and_call(self):
        feed = News('feed', 'title', datetime(2019, 11, 12), 'link', 'description', ['link_to_image'], datetime.now())
        feed_str_example = f'Feed: feed\nTitle: title\nDate: {datetime(2019, 11, 12)}\nLink: link\n\ndescription\n\nLinks:\n[1] link --feed\n[2] link_to_image --image\n'
        self.assertEqual(feed.__str__(), feed_str_example)
        self.assertEqual(feed(), ('feed', 'title', datetime(2019, 11, 12), 'link', 'description', ['link_to_image']))


if __name__ == '__main__':
    unittest.main()
