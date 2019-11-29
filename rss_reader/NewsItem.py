import json


class NewsItem:
    """
    Class which define characteristics of the News item.
    """

    _iter_number = 1

    # TODO: add description of the news item
    def __init__(self, title, link, date, images, links):
        """
        Initialise fields of the class.
        :param title: title of the news item.
        :param link: link, where that news item is situated.
        :param date: date, when this page was published.
        :param image: image, connected with that news item.
        :param links: links, connected with that news item.
        """
        self.title = title
        self.link = link
        self.date = date
        if images is not None:
            self.images = images
        else:
            self.images = list()
        self.links = links

    def get_images(self):
        """
        Get sting which describe all images, connected with that news item.
        :return: string with describing of all images.
        """
        res_str = ""
        if self.images is not None:
            for image in self.images[1:]:
                if image is not None:
                    res_str = res_str + "\n[{0}]: {1}\t (image)".\
                        format(self._iter_number, image.image_link)
                    self._iter_number += 1
                    res_str = res_str + "\n"
            return res_str
        else:
            return None

    def get_links(self):
        """
        Get string which describes all links, connected with that news item.
        :return: string with describing of all links.
        """
        res_str = ""
        if self.links is not None:
            for link in self.links:
                if link is not None:
                    res_str = res_str + "\n[{0}]: {1}\t (link)".format(self._iter_number, link)
                    self._iter_number += 1
            res_str = res_str + "\n"
        else:
            res_str = "There are no links"
        return res_str

    def __str__(self):
        return "Title: \t{0} \n" \
               "Date: \t{2}.\n" \
               "Link: \t{1}\n\n" \
               "[Image title: {3}]\n" \
               "Image link: {4}\n" \
               "Links: {5}\n" \
            .format(self.title, self.link, self.date,
                    self.images[0].image_title if self.images[0] is not None else "",
                    self.images[0].image_link if self.images[0] is not None else "",
                    self.get_links() + (self.get_images() if self.get_images() is not None else ""))

    def convert_to_json(self):
        """
        Make JSON format of the news item.
        :return: dict, which describe own JSON format of the news.
        """
        return {'News_Item': {'Title': self.title, 'Date': self.date, 'Link': self.link,
                              'Image Title': self.images[0].image_title if self.images[0] is not None else "",
                              'Image link': self.images[0].image_link if self.images[0] is not None else "",
                              'Links': self.get_links() + (self.get_images()
                                                           if self.get_images() is not None else "")}
                }

    def get_json_representation(self):
        """
        Get JSON representation of the news item.
        :return: JSON representation of the news item.
        """
        return json.dumps(self.convert_to_json())

    # TODO: Normal output
    def __repr__(self):
        return "NewsItem {" \
               "title = {0}, " \
               "link = {1}. }" \
            .format(self.title, self.link)
