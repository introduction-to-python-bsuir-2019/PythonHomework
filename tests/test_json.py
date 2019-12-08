import unittest
from datetime import datetime
from rss_reader.json_formatter import Json
from rss_reader.news import News


class TestNews(unittest.TestCase):
    def test_json(self):
        news = [News('feed', 'title', datetime(2019, 11, 12), 'link', 'description', ['link_to_image'], datetime.now())]
        json_example = '''\
{
    "News": [
        {
            "Feed0": {
                "Feed source": "feed",
                "Title": "title",
                "Date": "2019-11-12 00:00:00",
                "Link": "link",
                "Description": "description",
                "Media_content": "['link_to_image']"
            }
        }
    ]
}'''
        self.assertEqual(Json(news).__str__(), json_example)


if __name__ == '__main__':
    unittest.main()
