"""
This module is a parser of console arguments for this project.
"""
import argparse
from argparse import Namespace

import app


def get_args() -> Namespace:
    """
    Function, that parse console args.
    :return: An object that provides the values ​​of parsed arguments.
    """
    parser = argparse.ArgumentParser(description="It is a python command-line rss reader")
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", action="version", version=f"%(prog)s {app.__version__}", help="Print version info")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided", default=-1)
    parser.add_argument("--verbose", action="store_true", help="Print result as JSON in stdout", default=False)
    parser.add_argument("--json", action="store_true", help="Outputs verbose status messages", default=False)
    parser.add_argument("--length", type=int, help="Sets the length of each line of news output", default=120)
    parser.add_argument("--date", help="Search past news by date in format yeardaymonth (19991311)")
    parser.parse_args()
    args = parser.parse_args()
    return args
