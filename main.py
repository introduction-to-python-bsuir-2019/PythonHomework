import argparse
from RSS import RssAggregator
import logging


__version__="0.1.0"

def get_args():        
    parser=argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument('source', help="RSS URL")
    parser.add_argument("-v","--version", action="version", version="%(prog)s version {version}".format(version=__version__), default=None, help="Print version info")
    parser.add_argument("--json",action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=None, help="Limit news topics if this parameter provided")
    args = parser.parse_args()
    return args

def main():
    args=get_args()
    if args.verbose:
        logger = get_log()
    else:
        logger = logging.getLogger()
    rssobject=RssAggregator(args, logger)
    news=rssobject.get_news()    
    if args.version:
        print(args.version)
    if args.json:
        rssobject.print_json(news)
    else:
        rssobject.print_news(news) 
    
    logger.info("Exit")
     

def get_log():    
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
    
if __name__=="__main__":
    main() 
