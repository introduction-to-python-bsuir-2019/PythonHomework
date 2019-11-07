import requests
import argparse

from parser import Parser
from printer import Printer


class RSS_reader:
    ''' Main programm class '''
    def __init__(self, cmd_args):
        self.source = cmd_args.source
        self.limit = cmd_args.limit or None
        self.json_mode = cmd_args.json or False
        self.parser = Parser()
        self.printer = Printer()

    def get_feed_from_source(self):
        '''Get rss xml file from source and parse by self.parser'''
        request = requests.get(self.source)

        self.feed = self.parser.parse(request.content)
        if not self.limit:
            self.limit = len(self.feed) + 1

    def print_feed(self):
        if self.json_mode:
            self.printer.json_print(self.parser.get_json_feed(self.limit))
        else:
            self.printer.stdout_print(self.feed, self.limit)


if __name__ == "__main__":
    cmd_arg_parser = argparse.ArgumentParser(description='Pure Python comandline RSS reader')
    cmd_arg_parser.add_argument('source', help='RSS URL')
    cmd_arg_parser.add_argument('--version', help='Print version info',
                                action='version', version='RSS reader v0.1 by Alex_Yan')
    cmd_arg_parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    cmd_arg_parser.add_argument('--limit', type=int, help='Limit news topics if this parameter privided')
    cmd_arg_parser.add_argument('--verbose', help='Outputs verbose status messages')
    cmd_args = cmd_arg_parser.parse_args()

    reader = RSS_reader(cmd_args)
    reader.get_feed_from_source()
    reader.print_feed()
