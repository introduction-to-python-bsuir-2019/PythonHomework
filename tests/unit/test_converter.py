from unittest import TestCase
from unittest.mock import patch, call, Mock, mock_open
from pathlib import Path
from base64 import b64decode
from urllib.error import URLError
from datetime import datetime

from rssreader.converter import Converter, HTMLConverter, FB2Converter
from rssreader.feed import Feed
from rssreader.news import News


class ConverterTestCase(TestCase):
    """Test basic abstract class for any converter"""
    def test_init(self) -> None:
        mock_instance = Mock()
        self.converter = Converter.__init__(mock_instance, Path('path/to/cache'), Path('path/to/file'))
        self.assertListEqual([call._init_file_dir(), call._init_image_dir(Path('path/to/cache'))],
                             mock_instance.mock_calls)

    def test_init_file_dir_exist(self) -> None:
        """Test init when file already exists"""
        mock_instance = Mock()

        mock_instance.file_path.parent.exists.return_value = True
        Converter._init_file_dir(mock_instance)
        self.assertListEqual([call.file_path.parent.exists()], mock_instance.mock_calls)

    def test_init_file_dir_make(self) -> None:
        """Test init when file directory does not exist"""
        mock_instance = Mock()

        mock_instance.file_path.parent.exists.return_value = False
        Converter._init_file_dir(mock_instance)
        self.assertListEqual([call.file_path.parent.exists(), call.file_path.parent.mkdir(parents=True, exist_ok=True)],
                             mock_instance.mock_calls)

    def test_init_image_dir_exist(self) -> None:
        """Test init when image cache already exists"""
        mock_instance = Mock()
        mock_instance._get_image_binary = Mock(return_value='binary')

        mock_path = Mock(return_value='path/to/cache')
        mock_path.joinpath = Mock()
        mock_path.joinpath.return_value.exists.return_value = True

        Converter._init_image_dir(mock_instance, mock_path)

        # directory is not created
        self.assertNotIn(call().mkdir(parents=True, exist_ok=True), mock_path.joinpath.mock_calls)

        # check default image data
        self.assertEqual({'name': 'no_image.jpg', 'type': 'image/jpeg', 'url': '', 'data': 'binary'},
                         mock_instance._default_image)

    def test_init_image_dir_make(self) -> None:
        """Test init when image cache does not exist"""
        mock_instance = Mock()
        mock_path = Mock(return_value='path/to/cache')
        mock_path.joinpath = Mock()
        mock_path.joinpath.return_value.exists.return_value = False

        Converter._init_image_dir(mock_instance, mock_path)

        self.assertIn(call().mkdir(parents=True, exist_ok=True), mock_path.joinpath.mock_calls)

    def test_get_image_binary_make(self) -> None:
        with patch("builtins.open", mock_open(read_data=b'binary')) as mock_image:
            result = Converter._get_image_binary('path/to/image')

        mock_image.assert_called_with('path/to/image', 'rb')
        self.assertEqual(b'binary', b64decode(result))

    def test__obtain_image_ident(self) -> None:
        self.assertEqual(
            Converter._obtain_image_ident('https://test.com/1.jpg'), '1bef62681cbe8fb79a72834948c477cd.jpg')
        self.assertEqual(
            Converter._obtain_image_ident('https://test.com/2.jpg'), '8e3df14265973abe39396370d6ed6e6b.jpg')

    def test__download_image_ok(self) -> None:
        with patch('urllib.request.urlretrieve') as mock_urlretrieve:
            result = Converter._download_image('url/to/image', 'store/path')

        mock_urlretrieve.assert_called_with('url/to/image', 'store/path')
        self.assertTrue(result)

    def test_download_image_err(self) -> None:
        with patch('urllib.request.urlretrieve', side_effect=URLError('shutdown')) as mock_urlretrieve:
            result = Converter._download_image('url/to/image', 'store/path')

        mock_urlretrieve.assert_called_with('url/to/image', 'store/path')
        self.assertFalse(result)

    def test_save(self) -> None:
        fake_instance = Mock()
        fake_instance.file_path = 'path/to/file'
        mo = mock_open()

        with patch("builtins.open", mo, create=True) as mock_write:
            Converter._save(fake_instance, data='conversion result')

        mock_write.assert_called_with('path/to/file', 'w')
        mo().write.assert_called_once_with('conversion result')

    def test_perform(self) -> None:
        fake_instance = Mock()
        fake_instance._convert = Mock(return_value='data')
        Converter.perform(fake_instance, 'feed')
        self.assertListEqual([call._convert('feed'), call._save('data')], fake_instance.mock_calls)


class HTMLConverterTestCase(TestCase):
    """Test html converter"""
    def setUp(self) -> None:
        self.paths = [Path('cache/dir'), Path('file/path')]

        self.feed = Feed('https://dummy.xz/here.rss', None)
        self.feed.encoding = 'utf-8'
        self.feed.title = 'Dummy news'

        self.first_news = News(
            'First', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'text/html)', 'href': 'https://sdf/1'}]
        )

        self.second_news = News(
            'Second', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/2',
            'We are happy', [{'type': 'image/jpeg)', 'href': 'https://sdf/1.jpg'}]
        )

        self.feed.news.append(self.first_news)
        self.feed.news.append(self.second_news)

    def test_init(self) -> None:
        with patch('rssreader.converter.Converter.__init__') as mock_parent:
            instance = HTMLConverter(*self.paths)

        mock_parent.assert_called_once_with(*self.paths)
        self.assertTrue(hasattr(instance, 'book_template'))
        self.assertTrue(hasattr(instance, 'news_template'))
        self.assertTrue(hasattr(instance, 'href_template'))
        self.assertTrue(hasattr(instance, 'img_template'))

    def test_convert(self) -> None:
        """Test conversion result when no limit is applied"""
        fake_instance = Mock()
        self.feed.limit = None
        fake_instance._process_links = Mock(return_value=(['images|'], ['links|']))
        fake_instance.news_template.format = Mock(return_value='news|')
        fake_instance.book_template.format = Mock(return_value='HTML')
        result = HTMLConverter._convert(fake_instance, self.feed)

        self.assertTrue(result == 'HTML')

        # check processed links
        self.assertListEqual(
            [call([{'type': 'text/html)', 'href': 'https://sdf/1'}]),
             call([{'type': 'image/jpeg)', 'href': 'https://sdf/1.jpg'}])],
            fake_instance._process_links.mock_calls
        )

        # check news data to be applied to format
        self.assertListEqual(
            [call(title='First', description='Everything is ok', img='images|', hrefs='links|'),
             call(title='Second', description='We are happy', img='images|', hrefs='links|')],
            fake_instance.news_template.format.mock_calls
        )

        # check result call
        self.assertListEqual(
            [call(title='Dummy news', encoding='utf-8', news='news|\n    news|')],
            fake_instance.book_template.format.mock_calls
        )

    def test_convert(self) -> None:
        """Test conversion result when news limit is applied"""
        fake_instance = Mock()
        self.feed.limit = 1
        fake_instance._process_links = Mock(return_value=(['images|'], ['links|']))
        fake_instance.news_template.format = Mock(return_value='news|')
        fake_instance.book_template.format = Mock(return_value='HTML')
        result = HTMLConverter._convert(fake_instance, self.feed)

        self.assertTrue(result == 'HTML')

        # check processed links
        self.assertListEqual(
            [call([{'type': 'text/html)', 'href': 'https://sdf/1'}])],
            fake_instance._process_links.mock_calls
        )

        # check news data to be applied to format
        self.assertListEqual(
            [call(title='First', description='Everything is ok', img='images|', hrefs='links|')],
            fake_instance.news_template.format.mock_calls
        )

        # check result call
        self.assertListEqual(
            [call(title='Dummy news', encoding='utf-8', news='news|')],
            fake_instance.book_template.format.mock_calls
        )


class FB2ConverterTestCase(TestCase):
    """Test fb2 converter"""
    def setUp(self) -> None:
        self.paths = [Path('cache/dir'), Path('file/path')]

        self.feed = Feed('https://dummy.xz/here.rss', None)
        self.feed.encoding = 'utf-8'
        self.feed.title = 'Dummy news'

        self.first_news = News(
            'First', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'text/html)', 'href': 'https://sdf/1'}]
        )

        self.second_news = News(
            'Second', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/2',
            'We are happy', [{'type': 'image/jpeg)', 'href': 'https://sdf/1.jpg'}]
        )

        self.feed.news.append(self.first_news)
        self.feed.news.append(self.second_news)

    def test_init(self) -> None:
        with patch('rssreader.converter.Converter.__init__') as mock_parent:
            instance = FB2Converter(*self.paths)

        mock_parent.assert_called_once_with(*self.paths)
        self.assertTrue(hasattr(instance, 'book_template'))
        self.assertTrue(hasattr(instance, 'news_template'))
        self.assertTrue(hasattr(instance, 'image_template'))
        self.assertTrue(hasattr(instance, 'binary_template'))

    def test_convert(self) -> None:
        """Test conversion result when no limit is applied"""
        fake_instance = Mock()
        self.feed.limit = None
        fake_instance._process_links = Mock(return_value=(['binary|'], ['images|'], ['links|']))
        fake_instance.news_template.format = Mock(return_value='news|')
        fake_instance.book_template.format = Mock(return_value='FB2')
        fb2 = FB2Converter._convert(fake_instance, self.feed)

        self.assertTrue(fb2 == 'FB2')

        # check processed links
        self.assertListEqual(
            [call([{'type': 'text/html)', 'href': 'https://sdf/1'}]),
             call([{'type': 'image/jpeg)', 'href': 'https://sdf/1.jpg'}])],
            fake_instance._process_links.mock_calls
        )

        # check news data to be applied to format
        self.assertListEqual(
            [call(num=1, title='First', description='Everything is ok', images='images|', links='links|'),
             call(num=2, title='Second', description='We are happy', images='images|', links='links|')],
            fake_instance.news_template.format.mock_calls
        )

        # check result call
        self.assertListEqual(
            [call(title='Dummy news', prog='rssreader 0.5', url='https://dummy.xz/here.rss', encoding='utf-8',
                  sections='news|news|', binaries='binary|binary|')],
            fake_instance.book_template.format.mock_calls
        )

    def test_convert_limit(self) -> None:
        """Test conversion result when news limit is applied"""
        fake_instance = Mock()
        self.feed.limit = 1
        fake_instance._process_links = Mock(return_value=(['binary|'], ['images|'], ['links|']))
        fake_instance.news_template.format = Mock(return_value='news|')
        fake_instance.book_template.format = Mock(return_value='FB2')
        fb2 = FB2Converter._convert(fake_instance, self.feed)

        self.assertTrue(fb2 == 'FB2')

        # check processed links
        self.assertListEqual(
            [call([{'type': 'text/html)', 'href': 'https://sdf/1'}])],
            fake_instance._process_links.mock_calls
        )

        # check news data to be applied to format
        self.assertListEqual(
            [call(num=1, title='First', description='Everything is ok', images='images|', links='links|')],
            fake_instance.news_template.format.mock_calls
        )

        # check final conversion
        self.assertListEqual(
            [call(title='Dummy news', prog='rssreader 0.5', url='https://dummy.xz/here.rss', encoding='utf-8',
                  sections='news|', binaries='binary|')],
            fake_instance.book_template.format.mock_calls
        )
