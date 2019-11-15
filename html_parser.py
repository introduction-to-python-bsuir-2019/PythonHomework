from html.parser import HTMLParser

class _html_parser(HTMLParser):
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
                    self.links += [attr[1]]
        elif tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links += [attr[1]]

    def handle_data(self, data):
        self.text += data

def parse_HTML(text):
    parser = _html_parser();
    parser.feed(text)
    return parser.text, parser.links