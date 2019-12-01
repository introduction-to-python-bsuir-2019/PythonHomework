"""Entry point module"""

import logging

from rssreader.arguments import all_args, arg_verbose
from rssreader.parser import feed_parser
from rssreader.format_conversion import conversion_json as cv_json
from rssreader.format_conversion import conversion_html as cv_html
from rssreader.format_conversion import conversion_pdf as cv_pdf
from rssreader.db import news_database as db


class RssReader(all_args.Arguments):
    def __reaction_to_arguments(self) -> None:
        """
        Method that performs various actions
        depending on command line arguments
        """
        limit = self.args.limit
        source = self.args.source
        date = self.args.date
        to_html = self.args.to_html
        to_pdf = self.args.to_pdf
        colorize = self.args.colorize
        debug_string = "Start with arguments: " +\
            f"--limit: {limit}, " +\
            f"--json {self.args.json}, " +\
            f"--verbose {self.args.verbose}, " +\
            f"--date {date}, " +\
            f"--to-html {to_html}, " +\
            f"--to-pdf {to_pdf}, " +\
            f"--colorize {colorize}"

        logging.debug(debug_string)
        logging.debug(f"URL: {source}")

        feed = feed_parser.RssParser(source, limit)
        feed_json = cv_json.JsonConversion(source, limit)
        feed_db = db.NewsDatabase(source, date, limit)

        if limit is not None and limit < 1:
            msg = "Limit is less than one"
            logging.info(f"Stop. {msg}")
            return msg

        if date:
            news_from_db = feed_db.show_news()

            if news_from_db:
                if to_html and news_from_db:
                    feed_html = cv_html.HtmlConversion(news_from_db)
                    feed_html.save_html_news(feed_html.conversion_to_html())
                if to_pdf and news_from_db:
                    feed_pdf = cv_pdf.PdfConversion(news_from_db)
                    feed_pdf.conversion_to_pdf()
                if self.args.json:
                    return feed_json.convert_to_json(news_from_db)
                else:
                    if colorize:
                        return feed.make_pretty_rss_colorize(news_from_db)
                    else:
                        return feed.make_pretty_rss(news_from_db)
            else:
                msg = f"No news with date {date} and url {source}"
                logging.info(msg)
                return msg

        news_parsing = feed.parse_news()
        logging.info(f"Get rss from {source}")

        if self.args.json:
            logging.info(f"Convert rss from {source} to json")
            result = feed_json.convert_to_json(news_parsing)
        else:
            logging.info("Show result of parsing")
            if colorize:
                result = feed.make_pretty_rss_colorize(news_parsing)
            else:
                result = feed.make_pretty_rss(news_parsing)

        if to_html and news_parsing:
            feed_html = cv_html.HtmlConversion(news_parsing)
            feed_html.save_html_news(feed_html.conversion_to_html())

        if to_pdf and news_parsing:
            feed_pdf = cv_pdf.PdfConversion(news_parsing)
            feed_pdf.conversion_to_pdf()

        feed_db.update_news(news_parsing)
        return result

    def get_verbose(self):
        return arg_verbose.AppLogging.show_logs() if self.args.verbose else ""

    def run(self) -> None:
        """Application launch"""
        logging.info("Run app")
        return self.__reaction_to_arguments()


def main() -> None:
    """Main application method"""
    try:
        arg_verbose.AppLogging.log_setup()
        rss_app = RssReader()
        print(rss_app.run())
        print(rss_app.get_verbose())
    except Exception as e:
        logging.error(e)
        print(e)
