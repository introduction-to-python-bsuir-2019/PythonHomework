import xml.etree.ElementTree as tree
import xml.dom.minidom as minidom

from image_handler import get_image_as_base64

class FB2:
	''''''

	def __init__(self):
		self.root = tree.Element('FictionBook')
		self.root.set('xmlns:l', "http://www.w3.org/1999/xlink")

		self.description = tree.SubElement(self.root, 'description')
		self.body = tree.SubElement(self.root, 'body')

		self.image_iter = 0


	def create_xml_as_string(self):
		return (tree.tostring(self.root)).decode('ascii')


	def write_to_file(self, filepath: str) -> None:
		with open(filepath, 'w') as file:
			file.write(self.create_xml_as_string())

		pretty_string = minidom.parse(filepath).toprettyxml()
		
		with open(filepath, 'w') as file:
			file.write(pretty_string)


	def _add_image_binary(self, image_url: str, image_name: str):
		if image_url == '' or image_url == None:
			return

		binary = tree.SubElement(self.root, 'binary')
		binary.set('id', image_name)
		binary.set('content-type', 'image/png')
		binary.text = get_image_as_base64(image_url)


	def add_description_of_resource(self, title_info, subtitle_info, image_url):
		title = tree.SubElement(self.body, 'title')

		title_descr = tree.SubElement(title, 'p')
		subtitle_descr = tree.SubElement(self.body, 'p')

		title_descr.text = title_info
		subtitle_descr.text = subtitle_info

		self._add_image(self.body, image_url, 'cover.png')


	def _add_tag_p(self, parent, text):
		p = tree.SubElement(parent, 'p')
		p.text = text


	def _add_tag_emptyline(self, parent):
		tree.SubElement(parent, 'empty-line')


	def _add_image(self, parent, img_url, img_name):
		image = tree.SubElement(parent, 'image')
		image.set('l:href', '#' + img_name)

		self._add_image_binary(img_url, img_name)


	def add_section(self, title_info, date, link, img_link, content):
		section = tree.SubElement(self.body, 'section')
		title = tree.SubElement(section, 'title')
		
		self._add_tag_p(title, title_info)
		self._add_tag_p(section, date)
		self._add_tag_p(section, link)
		self._add_tag_emptyline(section)
		self._add_image(section, img_link, ('img' + str(self.image_iter) + '.png'))
		self._add_tag_emptyline(section)
		self._add_tag_p(section, content)

		self.image_iter += 1

