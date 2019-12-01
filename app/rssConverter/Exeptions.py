class RssGetError(Exception):
    """Class for exception in rss"""
    def __init__(self, url):
        self.url = url


class IncorrectLimit(Exception):
    """Class for exception in news limit"""
    def __init__(self, max_quantity):
        self.max_quantity = max_quantity


class IncorrectDateOrURL(Exception):
    """Class for exception in date of reading or url"""
    def __init__(self, date, url):
        self.date = date
        self.url = url


class IncorrectAddress(Exception):
    """Class for exception in address for saving file"""
    def __init__(self, address):
        self.address = address
