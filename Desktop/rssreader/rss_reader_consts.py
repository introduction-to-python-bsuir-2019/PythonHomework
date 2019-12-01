import os

PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))

NEWS_SEPARATOR_LEN = 100  # magic number
NEWS_SEPARATOR = '=' * NEWS_SEPARATOR_LEN


EN = '\n'  # enter
DEN = '\n\n'  # double enter

KEYWORD_FEED = 'Feed: '
KEYWORD_TITLE = 'Title: '
KEYWORD_DATE = 'Date: '
KEYWORD_LINK = 'Link: '
KEYWORD_IMGS_LINKS = "Image's links: "
KEYWORD_CONTENT = 'Short content: '


MONTHS = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

COLOR_WHITE = 'white'
COLOR_YELLOW = 'yellow'
COLOR_GREEN = 'green'
COLOR_BLUE = 'blue'
COLOR_RED = 'red'
