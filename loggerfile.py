import logging

def log():
    extra = {'app_name':'rss-reader'}
    logger = logging.getLogger(__name__)
    syslog = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(app_name)s : %(message)s')
    syslog.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(syslog)
    logging.basicConfig(filename="loggs.log", level=logging.DEBUG)
    return logging.LoggerAdapter(logger, extra)