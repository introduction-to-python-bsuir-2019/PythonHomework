class NewsItem:
    """
    Class which define characteristics of the News item.
    """

    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def __str__(self):
        return "Title : \t{0} \n" \
               "Description: \t{1} \n\n" \
               "Link: \t{2}.\n".format(self.title, self.description, self.link)

    def __repr__(self):
        return "NewsItem {" \
               "title = {0} \n" \
               "description = {1} \n" \
               "link = {2}.\n }"\
            .format(self.title, self.description, self.link)
