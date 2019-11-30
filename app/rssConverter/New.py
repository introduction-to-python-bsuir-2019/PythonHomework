class New:
    """Class for describing 1 new"""
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
    """Class for describing 1 image"""
    def __init__(self, csr):
        self.csr = csr
