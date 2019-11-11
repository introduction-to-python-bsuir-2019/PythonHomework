class Image:
    """
    Class which define basic characteristics of the Image.
    """

    def __init__(self, image_title, image_link):
        """
        Initialise fields of the Image class
        :param image_title: title, which describe image in that page.
        :param image_link: link, where you can find that image.
        """
        self.image_title = image_title
        self.image_link = image_link

    def get_image_link(self):
        """
        Get link, where image is situated in string format.
        :return:
        """
        return "Link: {0} (image)".format(self.image_link)

    def __str__(self):
        return "\n[Image: {0}]".format(self.image_title)

    def __repr__(self):
        return "Image {" \
               "image_title = {0}, \n" \
               "image_link = {1}. \n" \
               "}".format(self.image_title, self.image_link)
