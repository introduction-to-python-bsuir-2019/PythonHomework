class Image:
    """
    This class represents information about image like link and alternative text
    """

    def __init__(self, link, alt):
        self.link = link
        self.alt = alt

    def to_json(self):
        """
        This method converts Image object to JSON
        :return: dict
        """
        return {'link': self.link, 'alt': self.alt}

    @staticmethod
    def from_json(json_obj):
        """
        THis method gets Image object from JSON
        :param json_obj: dict
        :return: Image
        """
        if json_obj:
            return Image(json_obj.get('link', ''), json_obj.get('alt', ''))
