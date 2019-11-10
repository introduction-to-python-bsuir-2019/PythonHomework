import argparse


def get_args():
    parser = argparse.ArgumentParser(description="frbz(free reader by Zviger) - python command-line rss reader")
    parser.add_argument("source", help="RSS URL")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.parse_args()
    args = parser.parse_args()
    return args
