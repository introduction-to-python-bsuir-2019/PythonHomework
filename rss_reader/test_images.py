import unittest
from reader.Image import Image


class TestImage(unittest.TestCase):
    def setUp(self) -> None:
        self.image = Image('Image Title', 'title.com')

    def test_image_title(self):
        self.assertEqual(self.image.image_title, 'Image Title')

    def test_image_link(self):
        self.assertEqual(self.image.image_link, 'title.com')

    def test_get_image_link(self):
        self.assertEqual(self.image.get_image_link(),
                         'Link: {0} (image)'.format(self.image.image_link))


if __name__ == '__main__':
    unittest.main()
