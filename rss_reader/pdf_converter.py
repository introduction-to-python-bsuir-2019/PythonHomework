"""PDF converter module"""

import logging
import requests

from fpdf import SYSTEM_TTFONTS, FPDF

SYSTEM_TTFONTS = ''


class PDFConverter:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name
        self.pdf = FPDF(orientation='P', unit='mm', format='A4')

    def dump(self):
        """Create and fill PDF-file"""
        logging.info("Create and fill PDF-file")

        margin = 5

        self.pdf.add_page()
        self.pdf.set_auto_page_break(True, 10 * margin)

        for element in self.data:
            self.pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
            self.pdf.set_fill_color(62, 147, 96)

            self.pdf.set_text_color(255, 255, 255)
            self.pdf.set_font("FreeSans", size=14)
            self.pdf.multi_cell(0, 8, txt=element["title"], align="C", fill=1)
            self.pdf.set_fill_color(90, 167, 120)
            self.pdf.set_font("FreeSans", size=10)
            self.pdf.multi_cell(0, 5, txt=element["date"], align="R", fill=1)
            self.pdf.set_font("FreeSans", size=10)
            self.pdf.multi_cell(0, 5, txt=element["link"], align="R", fill=1)

            self.pdf.set_fill_color(229, 229, 229)
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.set_font("FreeSans", size=12)
            self.pdf.multi_cell(0, 6, txt=element["text"], align="J", fill=1)

            self.pdf.set_fill_color(242, 242, 242)
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.set_font("FreeSans", size=10)

            self.pdf.ln(margin)

            for href in element["hrefs"]:
                page_height = 300
                image_height = 50

                try:
                    if page_height - self.pdf.get_y() < image_height + margin:
                        self.pdf.add_page()

                    if href[-4:] == '.png':
                        self.pdf.image(href, x=self.pdf.get_x() + image_height + margin, y=self.pdf.get_y(),
                                       h=image_height)
                        self.pdf.ln(image_height + margin)
                except Exception:
                    logging.error('Cant get an image from url')

            self.pdf.multi_cell(0, margin, txt="", align="J")

        self.pdf.output(f'{self.file_name}.pdf')
