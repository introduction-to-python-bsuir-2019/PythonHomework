import os
import unittest
from unittest.mock import patch
from rss_reader.image import Image


class ImageTest(unittest.TestCase):

    def setUp(self) -> None:
        self.image = Image('https://image', 'alternative text')

    def test_link(self):
        self.assertEqual(self.image.link, 'https://image')

    def test_alt(self):
        self.assertEqual(self.image.alt, 'alternative text')

    def test_to_json(self):
        self.assertEqual(self.image.to_json(), {'link': 'https://image', 'alt': 'alternative text'})

    def test_from_json(self):
        json_img = {'link': 'https://image', 'alt': 'alternative text'}
        img = Image.from_json(json_img)
        self.assertEqual(img.link, self.image.link)
        self.assertEqual(img.alt, self.image.alt)

    def test_download(self):
        directory_path = 'directory'
        file_name = 'file_name.img'
        response = '123'
        with patch('requests.get') as requests_get_mock:
            requests_get_mock.return_value.content = response
            with patch('builtins.open') as file_mock:
                output_path = self.image.download(directory_path, file_name)
        requests_get_mock.assert_called_with(self.image.link)
        file_mock.assert_called_with(output_path, 'wb')
        file_mock.return_value.__enter__.return_value.write.assert_called_once_with(response)
        self.assertEqual(output_path, os.path.join(directory_path, file_name))


if __name__ == '__main__':
    unittest.main()
