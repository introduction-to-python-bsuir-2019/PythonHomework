class RssGetError(Exception):
    def __init__(self, url):
        self.url = url


class IncorrectLimit(Exception):
    def __init__(self, max_quantity):
        self.max_quantity = max_quantity
