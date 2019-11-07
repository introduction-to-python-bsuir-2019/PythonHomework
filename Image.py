class Image:
    """
    Class which define basic characteristics of the Image.
    """

    def __init__(self, image_url, image_title, image_link):
        self.image_url = image_url
        self.image_title = image_title
        self.image_link = image_link

    def get_image_link(self):
        return "Link: {0} (image)".format(self.image_link)

    def __str__(self):
        return "\n[Image: {0}]".format(self.image_title)

    def __repr__(self):
        return "Image {" \
               "image_url = {0}, \n" \
               "image_title = {1}, \n" \
               "image_link = {2}. \n" \
               "}".format(self.image_url, self.image_title, self.image_link)
