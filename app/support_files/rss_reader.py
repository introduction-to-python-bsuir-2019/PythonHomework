"""
This module contains class for fork with RSS.
"""
from app.support_files import (
    rss_parser,
    args_parser,
    format_converter,
    app_logger,
    db_manager,
    exeptions)
from app.support_files.file_manager import store_str_to_file
from app.support_files.config import APP_NAME


class Reader:

    """
    Class for fork with RSS.
    """
    @staticmethod
    def exec_console_args() -> None:
        """
        Execute console commands.
        """
        logger = app_logger.init_logger(APP_NAME)
        _args = args_parser.get_args()
        logger.disabled = not _args.verbose
        logger.info("Program started")
        source = _args.source.rstrip("/")
        logger.info(f"Parsing {source} started")
        parser = rss_parser.Parser(source)

        limit = _args.limit
        to_json = _args.json
        to_html_path = _args.to_html
        to_fb2_path = _args.to_fb2

        if limit < 1 and limit != -1:
            print("The limit must be -1 or greater than 0")
            return None

        logger.info("Connecting with database")
        db = db_manager.DBManager()
        if _args.date is None:
            try:
                feed = parser.parse_feed(limit)
            except ConnectionError as err:
                print(err)
                return None
            logger.info(f"Parsing {source} finished")

            logger.info("Loading parsed data to database is started")
            db.insert_feed(feed)
            logger.info("Loading parsed data to database is finished")
        else:
            logger.info("Load data from database is started")
            try:
                feed = db.find_feed_by_link_and_date(source, _args.date, limit)
            except exeptions.FindFeedError as err:
                print(err)
                return None
            except exeptions.DateError as err:
                print(err)
                return None
            logger.info("Load data from database is finished")

        len_each_line = _args.length
        if len_each_line < 60:
            print("The length must be greater than 60")
            return None
        converter = format_converter.Converter([feed])

        if to_html_path:
            logger.info("Saving data in html format in file is started")
            try:
                store_str_to_file(converter.to_html_format(), to_html_path, "html")
            except exeptions.DirExistsError as err:
                print(err)
                return None
            except exeptions.DirError as err:
                print(err)
                return None
            logger.info("Saving data in html format in file is finished")
        elif to_fb2_path:
            logger.info("Saving data in fb2 format in file is started")
            try:
                store_str_to_file(converter.to_fb2_format(), to_fb2_path, "fb2")
            except exeptions.DirExistsError as err:
                print(err)
                return None
            except exeptions.DirError as err:
                print(err)
                return None
            logger.info("Saving data in fb2 format in file is finished")
        else:
            if to_json:
                logger.info("Data is converted to json format and printing is started")
                print(converter.to_json_format(str_len=len_each_line))
            else:
                logger.info("Data is converted to console format and printing is started")
                print(converter.to_console_format(str_len=len_each_line))
            logger.info("Printing is finished")
        return None


if __name__ == "__main__":
    Reader.exec_console_args()
