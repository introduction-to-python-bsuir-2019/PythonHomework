class RssGetError(Exception):
    def __init__(self, url):
        self.url = url


class IncorrectLimit(Exception):
    def __init__(self, max_quantity):
        self.max_quantity = max_quantity


class IncorrectDateOrURL(Exception):
    def __init__(self, date, url):
        self.date = date
        self.url = url


class IncorrectAddress(Exception):
    def __init__(self, address):
        self.address = address
