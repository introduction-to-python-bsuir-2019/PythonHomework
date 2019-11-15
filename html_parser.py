from html.parser import HTMLParser


class _html_parser(HTMLParser):
    """Class using for parsing html-formatted text"""

    def __init__(self):
        super().__init__()
        self.links = []
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            num = len(self.links)+1
            self.text += f"[Image {num}: "
            for attr in attrs:
                if attr[0] == "alt":
                    self.text += attr[1] + f"][{num}]"
                elif attr[0] == "src":
                    self.links += [attr[1] + " (image)"]
        elif tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links += [attr[1] + " (text)"]

    def handle_data(self, data):
        self.text += data


def parse_HTML(text):
    """Return text without tags or links and a list with links"""
    parser = _html_parser()
    parser.feed(text)
    return parser.text, parser.links
