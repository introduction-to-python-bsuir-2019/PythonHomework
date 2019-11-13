import os
from fpdf import FPDF
from image_handler import save_image_by_url


TITLE_IMG_NAME = 'title.png'


class PDF(FPDF):
	# def __init__(self, title: str, title_img_url: str):


	def set_meta_info(self, title: str, title_img_url: str):
		self.title = title
		self.title_img_url = title_img_url

		self.iter = 0


	def garbage_collector(self):
		'''Removing temp files'''
		for index in range(self.iter):
			os.remove('temp' + str(index) + '.png')
		os.remove(TITLE_IMG_NAME)


	def write_to_file(self, filepath: str):
		self.garbage_collector()
		self.output(u'news.pdf')


	def header(self):
		save_image_by_url(self.title_img_url, TITLE_IMG_NAME)
		self.image(TITLE_IMG_NAME, 10, 8, 33)

		self.set_font("Arial", 'B', size=12)
		self.cell(100)
		self.cell(0, 5, txt=self.title, ln=1)

		self.ln(10)


	def footer(self):
		self.set_y(-10)
 
		self.set_font('Arial', 'I', 8)

		page = 'Page ' + str(self.page_no()) + '/{nb}'
		self.cell(0, 10, page, 0, 0, 'C')


	def _add_title_of_news(self, title: str) -> None:
		self.set_font('Times', 'B', size=13)
		self.multi_cell(0,10, txt=title)


	def _add_date_of_news(self, date: str) -> None:
		self.set_font('Times', size=12)
		self.multi_cell(0,10, txt=date)


	def _add_link_of_news(self, link: str) -> None:
		self.set_font('Arial','I', size=11)
		self.multi_cell(0,10, txt=link)


	def _add_content_of_news(self, content: str) -> None:
		self.set_font('Times', size=12)
		self.multi_cell(0,10, txt=content)


	def _add_img_of_news(self, img_url: str) -> None:
		save_image_by_url(img_url, 'temp' + str(self.iter) + '.png')
		self.image('temp' + str(self.iter) + '.png')

		self.iter += 1


	def add_piece_of_news(self, title: str, date:str, link: str, img_url: str, content: str):
		self.alias_nb_pages()
		self.add_page()

		self._add_title_of_news(title)
		self._add_date_of_news(date)
		self._add_link_of_news(link)
		if img_url != '':
			self._add_img_of_news(img_url)
		self._add_content_of_news(content)
