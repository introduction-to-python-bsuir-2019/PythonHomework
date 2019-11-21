import logging
extra = {'app_name':'rss_parser'}

logger = logging.getLogger(__name__)
syslog = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(app_name)s : %(message)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(syslog)
logging.basicConfig(filename="loggs.log", level=logging.DEBUG)

logger = logging.LoggerAdapter(logger, extra)