import json

from Image import Image


class NewsItem:
    """
    Class which define characteristics of the News item.
    """

    # TODO: add description of the news item
    def __init__(self, title, link, date, image, links):
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
        if image is not None:
            self.image = image
        else:
            self.image = Image('', '')
        self.links = links

    def get_title(self):
        """
        Get title of the news item
        :return: title of the news item.
        """
        return self.title

    def get_link(self):
        """
        Get link in which that page is situated.
        :return: link, where that page if situated.
        """
        return self.link

    def get_links(self):
        """
        Get string which describes all links, connected with that news item.
        :return: string with describing of all links.
        """
        iter_number = 1
        res_str = ""
        if self.links is not None:
            for link in self.links:
                if link is not None:
                    res_str = res_str + "\n[{0}]: {1}\t (link)".format(iter_number, link)
                    iter_number += 1
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
                       self.image.image_title, self.image.image_link, self.get_links())

    def convert_to_json(self):
        """
        Make JSON format of the news item.
        :return: dict, which describe own JSON format of the news.
        """
        return {'News_Item': {'Title': self.title, 'Date': self.date, 'Link': self.link,
                              'Image Title': self.image.image_title, 'Image link': self.image.image_link,
                              'Links': self.get_links()}
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
               "title = {0} \n" \
               "link = {1}.\n }"\
            .format(self.title, self.link)
