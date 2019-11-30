"""Module which provides interface of translating news to .fb2."""
import logging
import xml.etree.ElementTree as tree
import xml.dom.minidom as minidom
from xml.etree.ElementTree import Element

from rssreader.image_handle import get_image_as_base64


ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.' + __file__.replace('.py', '')


class FB2:
    """Class, which allows to translate news to .fb2 format."""

    CLASS_LOGGER_NAME = MODULE_LOGGER_NAME + '.FB2'

    def __init__(self):
        """Initialize xml-tree."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.__init__')
        logger.info('Initialize xml-tree')

        self.root = tree.Element('FictionBook')
        self.root.set('xmlns:l', "http://www.w3.org/1999/xlink")

        self.description = tree.SubElement(self.root, 'description')
        self.body = tree.SubElement(self.root, 'body')

        self.image_iter = 0

    def _get_xml_as_string(self) -> None:
        """Convert xml-tree to string."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._get_xml_as_string')
        logger.info('Convert xml-tree to string')

        return (tree.tostring(self.root)).decode('ascii')

    def write_to_file(self, filepath: str) -> None:
        """Write xml-tree to file with filepath."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.write_to_file')
        logger.info('Write xml-tree to file')

        with open(filepath, 'w') as file:
            file.write(self._get_xml_as_string())

        pretty_string = minidom.parse(filepath).toprettyxml()

        with open(filepath, 'w') as file:
            file.write(pretty_string)

    def _add_image_binary(self, image_url: str, image_name: str) -> None:
        """Insert binary-data of image to xml-tree."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_image_binary')
        logger.info('Insert binary-data of image to xml-tree')

        if image_url == '' or image_url is None:
            return

        binary = tree.SubElement(self.root, 'binary')
        binary.set('id', image_name)
        binary.set('content-type', 'image/png')
        binary.text = get_image_as_base64(image_url)

    def add_description_of_resource(self, title_info: str, subtitle_info: str, image_url: str) -> None:
        """Insert description of resource to xml-tree."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.add_description_of_resource')
        logger.info('Insert description of resource to xml-tree')

        title = tree.SubElement(self.body, 'title')

        title_descr = tree.SubElement(title, 'p')
        subtitle_descr = tree.SubElement(self.body, 'p')

        title_descr.text = title_info
        subtitle_descr.text = subtitle_info

        self._add_image(self.body, image_url, 'cover.png')

    def _add_tag_p(self, parent: Element, text: str) -> None:
        """Insert <p>{text}</p> in xml-tree with parent-node."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_tag_p')
        logger.info("Insert <p>text</p> in xml-tree with parent-node")

        p = tree.SubElement(parent, 'p')
        p.text = text

    def _add_tag_emptyline(self, parent: Element) -> None:
        """Insert <empty-line/> in xml-tree with parent-node."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_tag_emptyline')
        logger.info("Insert <empty-line/> in xml-tree with parent-node")

        tree.SubElement(parent, 'empty-line')

    def _add_image(self, parent: Element, img_url: str, img_name: str) -> None:
        """Insert <image l:href="#{img_name}"/> in xml-tree with parent-node."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_image')
        logger.info('Insert <image l:href="#img_name"/> in xml-tree with parent-node')

        image = tree.SubElement(parent, 'image')
        image.set('l:href', '#' + img_name)

        self._add_image_binary(img_url, img_name)

    def add_section(self, title_info: str, date: str, link: str, imgs_links: list, content: str) -> None:
        """Insert <section>{}</section> in xml-tree with parent-node."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.add_section')
        logger.info('Insert <section></section> in xml-tree with parent-node')

        section = tree.SubElement(self.body, 'section')
        title = tree.SubElement(section, 'title')

        self._add_tag_p(title, title_info)
        self._add_tag_p(section, date)
        self._add_tag_p(section, link)
        self._add_tag_emptyline(section)
        if imgs_links:  # if imgs_links list is not empty
            # for img_link in imgs_links:
            #     self._add_image(section, img_link, ('img' + str(self.image_iter) + '.png'))
            #     self.image_iter += 1
            self._add_image(section, imgs_links[0], ('img' + str(self.image_iter) + '.png'))
            self.image_iter += 1

        self._add_tag_emptyline(section)
        self._add_tag_p(section, content)
