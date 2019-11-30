import unittest
from unittest.mock import patch, Mock
import rss_reader.news as news
from rss_reader.image import Image


class NewsContentTest(unittest.TestCase):

    def setUp(self) -> None:
        self.text = 'text'
        self.images = [Image('http://link', 'alt')]
        self.links = ['link1', 'link2']
        self.news_content = news.NewsContent(self.text, self.images, self.links)

    def test_text(self):
        self.assertEqual(self.news_content.text, self.text)

    def test_images(self):
        self.assertEqual(self.news_content.images, self.images)

    def test_links(self):
        self.assertEqual(self.news_content.links, self.links)

    def test_to_json(self):
        json_news_content = {'text': self.text, 'images': [{'link': 'http://link', 'alt': 'alt'}], 'links': self.links}
        self.assertEqual(self.news_content.to_json(), json_news_content)

    def test_from_json(self):
        json_news_content = {'text': self.text, 'images': [{'link': 'http://link', 'alt': 'alt'}], 'links': self.links}
        news_content = news.NewsContent.from_json(json_news_content)
        self.assertEqual(news_content.links, self.news_content.links)
        self.assertTrue(len(news_content.images) == len(self.news_content.images))
        for img1, img2 in zip(news_content.images, self.news_content.images):
            self.assertDictEqual(img1.__dict__, img2.__dict__)
        self.assertEqual(news_content.text, self.news_content.text)

    @patch('rss_reader.news.BeautifulSoup')
    def test_get_content_from_html(self, bs_mock):
        bs_mock.return_value = Mock(text=self.text)
        bs_mock.return_value.find_all.side_effect = [[{'src': 'http://link', 'alt': 'alt'}],
                                                     [{'href': 'link1'}, {'href': 'link2'}]]
        news_content = news.NewsContent.get_content_from_html('html')
        bs_mock.assert_called_with('html', 'lxml')
        bs_mock.return_value.find_all.assert_any_call('img')
        bs_mock.return_value.find_all.assert_any_call('a')
        self.assertEqual(news_content.text, self.news_content.text)
        self.assertEqual(news_content.links, self.news_content.links)
        self.assertTrue(len(news_content.images) == len(self.news_content.images))
        for img1, img2 in zip(news_content.images, self.news_content.images):
            self.assertDictEqual(img1.__dict__, img2.__dict__)

    def test_to_str(self):
        str_content = f'[image 1: alt][3]text\n\n\nLinks:\n[1]: link1 (link)\n[2]: ' + \
                      'link2 (link)\n[3]: http://link (image)\n'
        self.assertEqual(str_content, str(self.news_content))


class NewsItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.content = news.NewsContent('text', [Image('link', 'alt')], ['link1', 'link2'])
        self.title = 'title'
        self.link = 'link'
        self.date = (2019, 11, 28, 15, 22, 41, 3, 332, 0)
        self.str_date = 'Thu, 28 Nov 2019 15:22:41 +0000'
        self.news_item = news.NewsItem(self.title, self.date, self.link, self.content)

    def test_title(self):
        self.assertEqual(self.news_item.title, self.title)

    def test_link(self):
        self.assertEqual(self.news_item.link, self.link)

    def test_date(self):
        self.assertEqual(self.news_item.date, self.date)

    def test_content(self):
        self.assertEqual(self.news_item.content, self.content)

    def test_to_json(self):
        json_news_item = {'title': self.title, 'date': self.date, 'source': self.link,
                          'content': self.content.to_json()}
        self.assertEqual(self.news_item.to_json(), json_news_item)

    def test_from_json(self):
        json_news_item = {'title': self.title, 'date': self.date, 'source': self.link,
                          'content': self.content.to_json()}
        news_item = news.NewsItem.from_json(json_news_item)
        self.assertEqual(news_item.title, self.news_item.title)
        self.assertEqual(news_item.date, self.news_item.date)
        self.assertEqual(news_item.link, self.news_item.link)
        self.assertEqual(news_item.content.text, self.news_item.content.text)
        self.assertEqual(news_item.content.links, self.news_item.content.links)
        self.assertTrue(len(news_item.content.images) == len(self.news_item.content.images))
        for img1, img2 in zip(news_item.content.images, self.news_item.content.images):
            self.assertDictEqual(img1.__dict__, img2.__dict__)

    def test_to_str(self):
        str_news_item = f'Title: {self.title}\nDate: {self.str_date}\nLink: {self.link}\n\n{self.content}'
        self.assertEqual(str(self.news_item), str_news_item)


class NewsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.source = 'source'
        self.count = 3
        self.news = news.News(self.source, self.count)

    def test_source(self):
        self.assertEqual(self.news.source, self.source)

    def test_count(self):
        self.assertEqual(self.news.count, self.count)

    @patch('feedparser.parse')
    @patch('rss_reader.news.NewsContent.get_content_from_html')
    def test_parse_news(self, get_content_mock, parse_mock):
        test_date = (2019, 11, 28, 15, 22, 41, 3, 332, 0)
        parse_mock.return_value = {'bozo': None, 'feed': {'title': 'title'},
                                   'entries': [{'title': 'title', 'published_parsed': test_date,
                                                'link': 'link', 'summary': 'summary'}]}
        get_content_mock.return_value = 'content'
        result_news = self.news.parse_news()
        parse_mock.assert_called_once()
        parse_mock.assert_called_with(self.news.source)
        get_content_mock.assert_called_with('summary')
        self.assertTrue(len(result_news) == 1)
        news_item = result_news[0]
        self.assertEqual(news_item.title, 'title')
        self.assertEqual(news_item.date, test_date)
        self.assertEqual(news_item.link, 'link')
        self.assertEqual(news_item.content, 'content')

    def test_get_count(self):
        self.assertEqual(len(self.news.items), self.news.get_count())

    def test_to_json(self):
        json_news = {'news': {'feed': self.news.feed, 'items': []}, 'source': self.news.source}
        self.assertEqual(self.news.to_json(), json_news)

    def test_from_json(self):
        json_news = {'news': {'feed': self.news.feed, 'items': []}, 'source': self.news.source}
        news_obj = news.News.from_json(json_news)
        self.assertEqual(news_obj.source, self.news.source)
        self.assertEqual(news_obj.items, self.news.items)
        self.assertEqual(news_obj.feed, self.news.feed)

    def test_to_str(self):
        str_news = f'\nFeed: {self.news.feed}\n\n'
        self.assertEqual(str(self.news), str_news)


if __name__ == '__main__':
    unittest.main()
