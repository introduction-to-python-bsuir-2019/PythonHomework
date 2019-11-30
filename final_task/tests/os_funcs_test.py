import os
import sys
import unittest
from unittest.mock import patch
from rss_reader.news import NewsItem, NewsContent
from rss_reader.image import Image
import rss_reader.os_funcs as os_funcs


class OSFuncsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.dir_path = 'directory'
        self.new_dir_name = 'new_name'

    @patch('os.path.exists')
    @patch('os.mkdir')
    def test_create_directory(self, mkdir_mock, path_exists_mock):

        path_exists_mock.side_effect = [True, False]
        result = os_funcs.create_directory(self.dir_path, self.new_dir_name)
        path_exists_mock.assert_any_call(self.dir_path)
        path = os.path.join(self.dir_path, self.new_dir_name)
        path_exists_mock.assert_any_call(path)
        mkdir_mock.assert_called_once()
        mkdir_mock.assert_called_with(path)
        self.assertEqual(result, path)

        path_exists_mock.side_effect = [False]
        result = os_funcs.create_directory(self.dir_path, self.new_dir_name)
        self.assertEqual(result, None)

        path_exists_mock.side_effect = [True, True]
        result = os_funcs.create_directory(self.dir_path, self.new_dir_name)
        self.assertEqual(result, path)

    def test_get_project_directory_path(self):
        self.assertEqual(os.path.dirname(sys.argv[0]), os_funcs.get_project_directory_path())

    @patch('rss_reader.image.Image.download')
    def test_download_images(self, download_mock):
        image = Image('link', 'alt')
        news_content = NewsContent('text', [image], [])
        news_item = NewsItem('title', 'date', 'link', news_content)
        img_path = os.path.join(self.dir_path, '0_0.jpeg')

        download_mock.return_value = img_path
        result = os_funcs.download_images(news_item, self.dir_path, 0)
        download_mock.assert_called_once()
        download_mock.assert_called_with(self.dir_path, '0_0.jpeg')

        self.assertEqual(result, [img_path])


if __name__ == '__main__':
    unittest.main()

