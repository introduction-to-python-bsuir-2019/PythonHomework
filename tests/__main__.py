import unittest
from main_test import TestRSS_reader
from parser_test import TestParser
import os


def load_tests(test_cases):
    test_loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for case in test_cases:
        suite.addTests(test_loader.loadTestsFromTestCase(case))
    test_runner = unittest.TextTestRunner()
    test_runner.run(suite)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    load_tests((TestParser, TestRSS_reader))
