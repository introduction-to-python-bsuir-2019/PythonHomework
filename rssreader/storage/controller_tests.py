import unittest

from .controller import StorageController

__all__ = ['StorageController']


class TestStorageController(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
