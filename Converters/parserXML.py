import logging
import xml.etree.ElementTree as tree
import xml.dom.minidom as minidom
from xml.etree.ElementTree import Element

from Converters.image_handle import ImageHandling


class FB2(ImageHandling):
    """Class, which allows to translate news to .fb2 format."""

    def __init__(self):
        """Initialize xml-tree."""
        logging.info('Initialize xml-tree...')

        self.root = tree.Element('FictionBook')
        self.root.set('xmlns:l', "http://www.w3.org/1999/xlink")
        self.description = tree.SubElement(self.root, 'description')
        self.body = tree.SubElement(self.root, 'body')
        self.temp_image = 'temp_img.jpg'
        self.image_iter = 1

    def _get_xml_as_string(self):
        """Convert xml-tree to string."""
        logging.info('Converting xml-tree into string')

        return (tree.tostring(self.root)).decode('ascii')

    def write_to_file(self, filepath: str):
        """Write xml-tree to file with filepath."""
        logging.info('Write xml-tree to file')

        with open(filepath, 'w') as file:
            file.write(self._get_xml_as_string())

        pretty_string = minidom.parse(filepath).toprettyxml()

        with open(filepath, 'w') as file:
            file.write(pretty_string)

    def _add_image_binary(self, image_url: str, image_name: str):
        """Insert binary-data of image to xml-tree."""
        logging.info('Insert binary-data of image to xml-tree')

        if image_url == '' or image_url is None:
            return

        binary = tree.SubElement(self.root, 'binary')
        binary.set('id', image_name)
        binary.set('content-type', 'image/png')
        binary.text = self.get_image_as_base64(image_url)

    def _add_tag_emptyline(self, parent: Element):
        """Insert <empty-line/> in xml-tree with parent-node."""
        logging.info("Insert <empty-line/> in xml-tree with parent-node")

        tree.SubElement(parent, 'empty-line')

    def add_description_of_resource(self, title_info: str, subtitle_info: str, image_url: str):
        """Insert description of resource to xml-tree."""
        logging.info('Insert description of resource to xml-tree')

        title = tree.SubElement(self.body, 'title')
        self._add_tag_emptyline(title)

        title_descr = tree.SubElement(title, 'p')
        subtitle_descr = tree.SubElement(self.body, 'p')

        title_descr.text = title_info
        self._add_tag_emptyline(title)
        subtitle_descr.text = subtitle_info

        self._add_image(self.body, image_url, 'cover.png')

    def _add_tag_p(self, parent: Element, text: str):
        """Insert <p>{text}</p> in xml-tree with parent-node."""
        logging.info("Insert <p>text</p> in xml-tree with parent-node")

        p = tree.SubElement(parent, 'p')
        p.text = text

    def _add_image(self, parent: Element, img_url: str, img_name: str):
        """Insert <image l:href="#{img_name}"/> in xml-tree with parent-node."""
        logging.info('Insert <image l:href="#img_name"/> in xml-tree with parent-node')

        image = tree.SubElement(parent, 'image')
        image.set('l:href', '#' + img_name)

        self._add_image_binary(img_url, img_name)

    def add_section(self, title_info: str, date: str, link: str, imgs_links: list, content: str):
        """Insert <section>{}</section> in xml-tree with parent-node."""
        logging.info('Insert <section></section> in xml-tree with parent-node')

        section = tree.SubElement(self.body, 'section')
        title = tree.SubElement(section, 'title')
        self._add_tag_p(title, title_info)
        self._add_tag_p(section, date)
        self._add_tag_p(section, link)
        self._add_tag_emptyline(section)
        try:
            self._add_image(section, imgs_links, ('image' + str(self.image_iter) + '.png'))
            self.image_iter += 1
        except FileNotFoundError:
            self._add_tag_emptyline(section)

        self._add_tag_emptyline(section)
        self._add_tag_p(section, content)

    def get_news_as_fb2(self, news_list: list, filepath: str, descript: list):
        """Get news as fb2.
        Takes arguments:
        limit:int - limit of news, which will be returned;
        filepath:str - path where news will be saved.
        """

        self.add_description_of_resource(descript[0], descript[1], descript[2])

        filepath = filepath + '.fb2'

        for piece_of_news in news_list:
            self.add_section(title_info=piece_of_news['title'],
                             date=piece_of_news['date'],
                             content=piece_of_news['description'],
                             link=piece_of_news['link'],
                             imgs_links=piece_of_news['image'])

        self.write_to_file(filepath)
