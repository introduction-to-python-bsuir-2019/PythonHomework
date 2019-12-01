import unittest
import os
import logging
from app.rssConverter.main import creating_image_dir


class MainTests(unittest.TestCase):
    """Class for testing main class"""

    def test_image_dir_creating(self):
        """Test creation directory for images"""
        current_dir = os.getcwd()
        logger = logging.getLogger('main-test')
        self.image_path = os.path.join(current_dir, 'images')
        self.assertEqual(self.image_path, creating_image_dir(logger))


if __name__ == '__main__':
    unittest.main()
