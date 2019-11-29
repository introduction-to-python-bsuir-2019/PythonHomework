from html.parser import HTMLParser


class _HTMLTagsParser(HTMLParser):
    """Class using for parsing html-formatted text"""

    def __init__(self):
        super().__init__()
        self.links = []
        self.text = ""

    def handle_starttag(self, tag, attrs):
        """Convert <a> and <img> tags to text form"""
        if tag == "img":
            num = len(self.links)+1
            self.text += "[Image"
            for attr in attrs:
                if attr[0] == "alt" and attr[1] != "":
                    self.text += f": {attr[1]}"
                elif attr[0] == "src":
                    self.links += [attr[1] + " (image)"]
            self.text +=  f"][{num}]"
        elif tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links += [attr[1] + " (text)"]

    def handle_data(self, data):
        """Take text from HTML"""
        self.text += data


def parse_HTML(text):
    """Return text without tags or links and a list with links"""
    parser = _HTMLTagsParser()
    parser.feed(text)
    return parser.text, parser.links
