from unittest import TestCase
from unittest.mock import Mock, patch, call
from pathlib import Path
from urllib.error import URLError, HTTPError
from datetime import datetime

from bs4 import BeautifulSoup as bs

from rssreader.converter import Converter, HTMLConverter, FB2Converter
from rssreader.feed import Feed
from rssreader.news import News


class ConverterTestCase(TestCase):
    def setUp(self) -> None:
        self.test_dir = Path().cwd().joinpath('tmp_tests')
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self) -> None:
        self.test_dir.rmdir()

    def test__get_image_binary(self) -> None:
        img_path = self.test_dir.joinpath('img.png')
        self.assertFalse(img_path.exists())  # an image does not exist

        with open(img_path, 'wb') as file:
            file.write(b'image')

        self.assertEqual(Converter._get_image_binary(img_path), 'aW1hZ2U=')
        img_path.unlink()

    def mock_urlretrieve_ok(url, img_path) -> None:
        with open(img_path, 'wb') as img:
            img.write(b'image')

    @patch('urllib.request.urlretrieve', side_effect=mock_urlretrieve_ok)
    def test__download_image_ok(self, mocked_request) -> None:
        img_path = self.test_dir.joinpath('img.png')
        self.assertFalse(img_path.exists())  # an image does not exist

        self.assertTrue(Converter._download_image(None, image_path=img_path))
        mocked_request.assert_called_once_with(None, img_path)
        self.assertTrue(img_path.is_file())
        img_path.unlink()

    def mock_urlretrieve_error(url, img_path) -> None:
        if url == 'URL':
            raise URLError('url Error')
        elif url == 'HTTP':
            raise HTTPError(msg='http error', code=404, fp=None, hdrs='', url='some')
        else:
            raise Exception('Unknown error')

    @patch('urllib.request.urlretrieve', side_effect=mock_urlretrieve_error)
    def test__download_image_error(self, mocked_request) -> None:
        img_path = self.test_dir.joinpath('img.png')
        self.assertFalse(img_path.exists())  # an image does not exist

        self.assertFalse(Converter._download_image('URL', image_path=img_path))
        mocked_request.assert_called_once_with('URL', img_path)
        self.assertFalse(img_path.is_file())

        self.assertFalse(Converter._download_image('HTTP', image_path=img_path))
        self.assertFalse(img_path.is_file())

        with self.assertRaises(Exception) as cm:
            Converter._download_image('Another', image_path=img_path)


class HTMLConverterTestCase(TestCase):
    def setUp(self) -> None:
        self.test_dir = Path().cwd().joinpath('tmp_tests')
        self.test_dir.mkdir(exist_ok=True)

        self.feed = Feed('https://dummy.xz/here.rss', None)
        self.feed.encoding = 'utf-8'
        self.feed.title = 'Dummy news'

        self.first_news = News(
            'First', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'text/html)', 'href': 'https://sdf.dummy.xz/details_1'}]
        )

        self.second_news = News(
            'Second', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/2',
            'We are happy', []
        )

        self.feed.news.append(self.first_news)
        self.feed.news.append(self.second_news)

        self.file_path = self.test_dir.joinpath('news.html')
        self.assertFalse(self.file_path.is_file())  # this file does not exist

    def tearDown(self) -> None:
        self.test_dir.joinpath('images', 'no_image.jpg').unlink()
        self.test_dir.joinpath('images').rmdir()
        self.test_dir.rmdir()

    def test__converter(self) -> None:
        html_conv = HTMLConverter(self.test_dir, self.file_path)

        result = bs(html_conv._convert(self.feed), "html.parser")
        # check head
        self.assertEqual(result.find('title').text, 'Offline rss')

        # check body
        self.assertEqual(result.find('h1').text, self.feed.title)

        html_news = result.find_all('h4')
        self.assertEqual(len(html_news), 2)

        for i in range(0, len(html_news)):
            with self.subTest(i=i):
                self.assertEqual(html_news[i].text, self.feed.news[i].title + self.feed.news[i].description)

    def test__converter_limited(self) -> None:
        """News count is limited by limit argument"""
        self.feed.limit = 1
        html_conv = HTMLConverter(self.test_dir, self.file_path)

        result = bs(html_conv._convert(self.feed), "html.parser")
        # check head
        self.assertEqual(result.find('title').text, 'Offline rss')

        # check body
        self.assertEqual(result.find('h1').text, self.feed.title)

        html_news = result.find_all('h4')
        self.assertEqual(len(html_news), 1)


class FB2ConverterTestCase(TestCase):
    def setUp(self) -> None:
        self.test_dir = Path().cwd().joinpath('tmp_tests')
        self.test_dir.mkdir(exist_ok=True)

        self.feed = Feed('https://dummy.xz/here.rss', None)
        self.feed.encoding = 'utf-8'
        self.feed.title = 'Dummy news'

        self.first_news = News(
            'First', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'text/html)', 'href': 'https://sdf.dummy.xz/details_1'}]
        )

        self.second_news = News(
            'Second', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/2',
            'We are happy', []
        )

        self.feed.news.append(self.first_news)
        self.feed.news.append(self.second_news)

        self.file_path = self.test_dir.joinpath('news.fb2')
        self.assertFalse(self.file_path.is_file())  # this file does not exist

    def tearDown(self) -> None:
        self.test_dir.joinpath('images', 'no_image.jpg').unlink()
        self.test_dir.joinpath('images').rmdir()
        self.test_dir.rmdir()

    def test__converter(self) -> None:
        fb2_conv = FB2Converter(self.test_dir, self.file_path)

        result = bs(fb2_conv._convert(self.feed), "html.parser")

        self.assertEqual(result.find('book-title').text, self.feed.title)

        fb2_news = result.find_all('section')
        self.assertEqual(len(fb2_news), 2)

        self.assertEqual(fb2_news[0].text, '\n1. First\n\nEverything is ok\nMore information on: '
                                           'https://sdf.dummy.xz/details_1\n')
        self.assertEqual(fb2_news[1].text, '\n2. Second\n\nWe are happy\nMore information on: \n')

    def test__converter_limited(self) -> None:
        """News count is limited by limit argument"""
        self.feed.limit = 1

        fb2_conv = FB2Converter(self.test_dir, self.file_path)

        result = bs(fb2_conv._convert(self.feed), "html.parser")

        fb2_news = result.find_all('section')
        self.assertEqual(len(fb2_news), 1)
