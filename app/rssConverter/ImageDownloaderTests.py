import unittest
import os
from app.rssConverter.ImageDownloader import ImageDownloader


class ImageDownloaderTests(unittest.TestCase):
    """Class for testing images downloading and converting"""

    def setUp(self):
        current_dir = os.getcwd()
        self.temp_image_path = os.path.join(current_dir, 'temp_images')
        if not os.path.exists(self.temp_image_path):
            os.makedirs(self.temp_image_path)

    def tearDown(self):
        if os.path.exists(self.temp_image_path):
            file_list = [file for file in os.listdir(self.temp_image_path)]
            for file in file_list:
                pass
                os.remove(os.path.join(self.temp_image_path, file))
        os.removedirs(self.temp_image_path)

    def test_download_image(self):
        """Test image downloading"""
        self.result_string = os.path.join(self.temp_image_path, "avtobus_v_zabai_kale")
        self.assertEqual(self.result_string, ImageDownloader.download_image("https://img.tyt.by/thumbnails/n"
                                                                            "/03/e/avtobus_v_zabai_kale.jpg",
                                                                            self.temp_image_path))

    def test_get_image(self):
        """Test image getting"""
        with(open("BinaryImageTest", "r")) as file:
            result_binary_string = file.read()
        self.assertEqual(result_binary_string[:-1], ImageDownloader.get_image("https://img.tyt.by/thumbnails/n"
                                                                              "/03/e/avtobus_v_zabai_kale.jpg",
                                                                              self.temp_image_path))

    def test_convert_image_to_binary(self):
        """Test image convertation to binary format"""
        with(open("BinaryImageTest", "r")) as file:
            result_binary_string = file.read()
        result_path = os.path.join(self.temp_image_path, "avtobus_v_zabai_kale")
        self.assertEqual(result_binary_string[:-1], ImageDownloader.convert_image_to_binary(result_path))


if __name__ == '__main__':
    unittest.main()
