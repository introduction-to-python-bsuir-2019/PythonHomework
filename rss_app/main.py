"""
The main file to run the script
"""


import argparse
from rss_app.RSS import RssAggregator
from rss_app.converter import Converter
import logging
from datetime import datetime


__version__="0.4.0"

def get_args():

    """ Reads and returns arguments """

    parser=argparse.ArgumentParser( description="Pure Python command-line RSS reader.")
    parser.add_argument('source', help="RSS URL")
    parser.add_argument("-v","--version", action="version", version="%(prog)s version {version}".format(version=__version__), default=None, help="Print version info")
    parser.add_argument("--json",action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=None, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=str, help="For example: --date 20191020")
    parser.add_argument("--to-pdf", type=str, help='This argument receives the path where new file will be saved in format pdf.' + 
                        'For example: --to-pdf d:/news.pdf')
    parser.add_argument("--to-html", type=str, help="This argument receives the path where new file will be saved in format html." +
                        "For example: --to-html d:/news.html")
    args = parser.parse_args()
    return args

def main():

    """ Reads arguments and print news """

    args=get_args()
    if args.version:
        print(args.version)
    if args.verbose:
        logger = get_log()
    else:
        logger = logging.getLogger()
    rssobject=RssAggregator(args, logger)
    converter=Converter(args, logger)
    news=rssobject.get_news()
    if args.to_pdf:
        news_for_converter_pdf=rssobject.get_news_for_converter() 
        converter.pdf_converter(news_for_converter_pdf)
    if args.to_html:
        news_for_converter_html=rssobject.get_news_for_converter() 
        converter.html_converter(news_for_converter_html)
    if args.date:
        try:
            datetime.strptime(args.date, "%Y%m%d")
            data = rssobject.get_from_json_file()
            rssobject.print_news_from_file(data)
            return
        except ValueError:
            print("ValueError: Time data {} does not match format %Y%m%d".format(args.date))
            return       
    if args.json:
        rssobject.print_json(news)        
    else:
        rssobject.print_news(news) 
    logger.info("Exit")
     

def get_log():
    
    """ Returns logger with DEBUG level for creating logs in stdout """

    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
    
if __name__=="__main__":
    main() 
