from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock

from rss_reader.converter import Converter


class TestConverter(TestCase):

    def setUp(self):
        title = "test"
        entries = MagicMock()
        out_dir = "_test"
        self.converter = Converter(title, entries, out_dir)

    # def test__create_directories(self):
    #     image_dir = "test"
    #     self.converter._create_directories(image_dir)
    #     self.fail()

    # def test__download_image(self):
    #     self.fail()

    def test__replace_urls_to_local_path(self):
        self.converter._download_image = MagicMock(return_value="test.jpg")
        mock_entry = MagicMock
        mock_entry.summary = '<img align="left" alt="Фото: Дарья Бурякина" border="0" height="48" hspace="5"' \
                             ' src="https://img.tyt.by/thumbnails/n/sport/0d/0/krivko_2019_4.jpg" width="72"/>' \
                             'Первый этап Кубка мира по биатлону продолжится женской спринтерской гонкой на 7,5 км.' \
                             '<br clear="all"/>'
        mock_entry_replaced = MagicMock()
        mock_entry_replaced.summary = f'<img align="left" alt="Фото: Дарья Бурякина" border="0" height="48"' \
            f' hspace="5" src="{self.converter.image_dir}/test.jpg" width="72"' \
            f'/>Первый этап Кубка мира по биатлону продолжится женской спринтерской гонкой' \
            f' на 7,5 км.<br clear="all"/>'
        entry = self.converter._replace_urls_to_local_path(mock_entry)
        self.assertEqual(mock_entry_replaced.summary, entry.summary)

    def test__replace_urls_to_absolute_path(self):
        self.converter._download_image = MagicMock(return_value="test.jpg")
        mock_entry = MagicMock
        mock_entry.summary = '<img align="left" alt="Фото: Дарья Бурякина" border="0" height="48" hspace="5"' \
                             ' src="https://img.tyt.by/thumbnails/n/sport/0d/0/krivko_2019_4.jpg" width="72"/>' \
                             'Первый этап Кубка мира по биатлону продолжится женской спринтерской гонкой на 7,5 км.' \
                             '<br clear="all"/>'
        mock_entry_replaced = MagicMock()
        image_path = (Path(self.converter.out_dir) / self.converter.temp_image_dir / 'test.jpg').absolute()
        mock_entry_replaced.summary = f'<img align="left" alt="Фото: Дарья Бурякина" border="0" height="48"' \
            f' hspace="5" ' \
            f'src="{image_path}" width="72"' \
            f'/>Первый этап Кубка мира по биатлону продолжится женской спринтерской гонкой' \
            f' на 7,5 км.<br clear="all"/>'
        entry = self.converter._replace_urls_to_absolute_path(mock_entry)
        self.assertEqual(mock_entry_replaced.summary, entry.summary)

    def test__generate_html(self):
        self.fail()

    # def test_entries_to_html(self):
    #     self.fail()
    #
    # def test_entries_to_pdf(self):
    #     self.fail()
    #
    # def test_entries_to_epub(self):
    #     self.fail()
