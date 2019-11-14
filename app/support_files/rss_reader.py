import logging
import sys
from . import rss_parser, args_parser, format_converter


class Reader:

    @staticmethod
    def exec_console_args():
        logger = logging.getLogger("console_app")
        logger.setLevel(logging.INFO)
        # create the logging file handler
        fh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        fh.setFormatter(formatter)
        # add handler to logger object
        logger.addHandler(fh)

        _args = args_parser.get_args()
        logger.disabled =  not _args.verbose
        logger.info("Program started")

        logger.info(f"Parsing {_args.source} started")
        parser = rss_parser.Parser(_args.source)

        limit = _args.limit
        to_json = _args.json

        if limit < 1 and limit != -1:
            print("The limit must be -1 or greater than 0")
            return

        feeds = [parser.parse_feed(limit)]
        if feeds[0] is None:
            print("Invalid url.")
            return
        logger.info(f"Parsing {_args.source} finished")

        len_each_line = _args.length
        if len_each_line < 60:
            print("The length must be greater than 60")
            return
        converter = format_converter.Converter(feeds)
        if to_json:
            logger.info("Data is converted to json format and printing is started")
            print(converter.to_json_format(str_len=len_each_line))
        else:
            logger.info("Data is converted to console format and printing is started")
            print(converter.to_console_format(str_len=len_each_line))
        logger.info("Printing is stoped")


if __name__ == "__main__":
    Reader.exec_console_args()
