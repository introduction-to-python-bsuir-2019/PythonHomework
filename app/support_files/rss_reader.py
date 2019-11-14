"""
This module contains class for fork with RSS.
"""
from app.support_files import rss_parser, args_parser, format_converter, app_logger


class Reader:

    """
    Class for fork with RSS.
    """
    @staticmethod
    def exec_console_args():
        """
        Execute console commands.
        """
        logger = app_logger.init_logger("console_app")
        _args = args_parser.get_args()
        logger.disabled = not _args.verbose
        logger.info("Program started")
        logger.info(f"Parsing {_args.source} started")
        parser = rss_parser.Parser(_args.source)

        limit = _args.limit
        to_json = _args.json

        if limit < 1 and limit != -1:
            print("The limit must be -1 or greater than 0")
            return None

        try:
            feed = parser.parse_feed(limit)
        except ConnectionError as err:
            print(err)
            return None
        logger.info(f"Parsing {_args.source} finished")

        len_each_line = _args.length
        if len_each_line < 60:
            print("The length must be greater than 60")
            return None
        converter = format_converter.Converter([feed])
        if to_json:
            logger.info("Data is converted to json format and printing is started")
            print(converter.to_json_format(str_len=len_each_line))
        else:
            logger.info("Data is converted to console format and printing is started")
            print(converter.to_console_format(str_len=len_each_line))
        logger.info("Printing is stoped")


if __name__ == "__main__":
    Reader.exec_console_args()
