"""Tests for rssreader.exceptions.all_exceptions module"""

import unittest


from rssreader.exceptions import all_exceptions as all_exc


class ThrowingArgumentParserTestCase(unittest.TestCase):
    """Test cases for ThrowingArgumentParser class"""
    def setUp(self):
        self.args_test = all_exc.ThrowingArgumentParser("test", "test")

    def test_error(self):
        """Function test_error test"""
        self.assertRaises(
            all_exc.ArgumentParserError,
            lambda: self.args_test.error("test")
            )


if __name__ == "__main__":
    unittest.main()
