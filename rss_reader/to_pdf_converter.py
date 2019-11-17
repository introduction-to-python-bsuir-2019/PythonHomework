"""Module which provides interface of translating news to .pdf."""
import os
from fpdf import FPDF
from image_handler import save_image_by_url


TITLE_IMG_NAME = 'title.png'


def _convert_to_latin_1(string: str) -> str:
	"""Convert to latin-1 encoding."""
	return string.encode('latin-1', 'replace').decode('latin-1')


class PDF(FPDF):
	"""Class, which allows to translate news to .pdf format."""

	def set_meta_info(self, title: str, title_img_url: str):
		"""Set information of rss-resource."""
		self.title = _convert_to_latin_1(title)
		self.title_img_url = title_img_url

		self.iter = 0


	def _garbage_collect(self):
		"""Remove temp img-files."""
		for index in range(self.iter):
			os.remove('temp' + str(index) + '.png')
		if self.title_img_url != '':
			os.remove(TITLE_IMG_NAME)


	def write_to_file(self, filepath: str):
		"""Write to file pdf items."""
		self._garbage_collect()
		self.output('news.pdf')


	def header(self):
		"""Set header of each page."""
		if self.title_img_url != '':
			save_image_by_url(self.title_img_url, TITLE_IMG_NAME)
			self.image(TITLE_IMG_NAME, 10, 8, 33)

		self.set_font("Arial", 'B', size=12)
		self.cell(100)
		self.cell(0, 5, txt=self.title, ln=1)

		self.ln(10)


	def footer(self):
		"""Set footer of each page."""
		self.set_y(-10)
 
		self.set_font('Arial', 'I', 8)

		page = 'Page ' + str(self.page_no()) + '/{nb}'
		self.cell(0, 10, page, 0, 0, 'C')


	def _add_title_of_news(self, title: str) -> None:
		"""Insert title of piece of news."""
		self.set_font('Times', 'B', size=13)
		self.multi_cell(0,10, txt=_convert_to_latin_1(title))


	def _add_date_of_news(self, date: str) -> None:
		"""Insert date of piece of news."""
		self.set_font('Times', size=12)
		self.multi_cell(0,10, txt=_convert_to_latin_1(date))


	def _add_link_of_news(self, link: str) -> None:
		"""Insert link of piece of news."""
		self.set_font('Arial','I', size=11)
		self.multi_cell(0,10, txt=_convert_to_latin_1(link))


	def _add_content_of_news(self, content: str) -> None:
		"""Insert content of piece of news."""
		self.set_font('Times', size=12)
		self.multi_cell(0,10, txt=_convert_to_latin_1(content))


	def _add_img_of_news(self, img_url: str) -> None:
		"""Insert image of piece of news."""
		save_image_by_url(img_url, 'temp' + str(self.iter) + '.png')
		self.image('temp' + str(self.iter) + '.png', None, None)

		self.iter += 1


	def add_piece_of_news(self, title: str, date:str, link: str, img_url: str, content: str):
		"""Insert piece of news to pdf."""
		self.alias_nb_pages()
		self.add_page()

		self._add_title_of_news(title)
		self._add_date_of_news(date)
		self._add_link_of_news(link)
		if img_url != '':
			self._add_img_of_news(img_url)
		self._add_content_of_news(content)
