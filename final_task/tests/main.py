import os
import unittest

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    start_directory = os.path.dirname(__file__)
    suite = test_loader.discover(start_directory)
    tests = unittest.TextTestRunner()
    tests.run(suite)
