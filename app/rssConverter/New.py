class New:
    def __init__(self):
        self.items = {'title': None,
                      'summary': None,
                      'link': None,
                      'pubDate': None,
                      'published': None,
                      'images': None,
                      'links': None,
                      }


class Image:
    def __init__(self, csr):
        self.csr = csr
