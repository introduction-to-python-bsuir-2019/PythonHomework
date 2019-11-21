"""
This module contains class for fork with RSS.
"""
from app.support_files import (
    rss_parser,
    args_parser,
    format_converter,
    app_logger,
    database,
    exeptions)


class Reader:

    """
    Class for fork with RSS.
    """
    @staticmethod
    def exec_console_args() -> None:
        """
        Execute console commands.
        """
        logger = app_logger.init_logger("console_app")
        _args = args_parser.get_args()
        logger.disabled = not _args.verbose
        logger.info("Program started")
        source = _args.source.rstrip("/")
        logger.info(f"Parsing {source} started")
        parser = rss_parser.Parser(source)

        limit = _args.limit
        to_json = _args.json

        if limit < 1 and limit != -1:
            print("The limit must be -1 or greater than 0")
            return None

        logger.info("Connecting with database")
        db = database.DB()
        if _args.date is None:
            try:
                feed = parser.parse_feed(limit)
            except ConnectionError as err:
                print(err)
                return None
            logger.info(f"Parsing {source} finished")

            logger.info("Loading parsed data to database")
            db.insert_feed(feed)
        else:
            logger.info("Load data from database")
            try:
                feed = db.find_feed_by_link_and_date(source, _args.date, limit)
            except exeptions.FindFeedError as err:
                print(err)
                return None
            except exeptions.DateError as err:
                print(err)
                return None

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
        logger.info("Printing is stopped")


if __name__ == "__main__":
    Reader.exec_console_args()
