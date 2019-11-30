"""Module contains objects related to PDF"""
import logging
import os
from typing import Dict, Any

import requests
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase import pdfmetrics

from rss_reader_ft.conversion.format_converter import FormatConverter


class PdfConverter(FormatConverter):
    """
    JsonConverter class
    inherited from FormatConverter abstract class.
    """
    def __init__(self, rss_feed_dict: Dict[str, Any]):
        """Init PdfConverter class"""
        self.convert_data: Dict[str, Any] = rss_feed_dict

    def convert_to_format(self) -> None:
        """Сonversion method to PDF format"""
        logging.info('Convert data to PDF and return it')

        file_name = "News_feed.pdf"
        self._generate_pdf_file(file_name)

    def _generate_pdf_file(self, file_name) -> None:
        logging.info('Generate_pdf_file')
        """
        Method to generate PDF file

        If you wonder why he did not support the Russian language, I will answer you,
        because the stars are not on my side and the moon is in the wrong phase,
        I tried to connect the font DejaVuSans.ttf with a friend,
        but it does not work like several other options that were on the internet.
        Therefore, he works only with the Latin alphabet and sometimes there are articles with some data
        that he does not want to convert.
        8:00 AM scream of the soul (((
        """

        pdf_file = canvas.Canvas(file_name, landscape(letter))
        pdfmetrics.registerFont(TTFont('DVS', 'DejaVuSans.ttf'))

        pdf_file.setFont('DVS', 24, leading=None)
        pdf_file.drawCentredString(415, 250, self.convert_data['Feed'])

        pdf_file.setFont('DVS', 24, leading=None)
        pdf_file.drawCentredString(415, 200, self.convert_data['Url'])
        pdf_file.showPage()

        for count, news in enumerate(self.convert_data['News']):
            y = self._edit_text(pdf_file, 500, news['Title'])

            for img in news["Links"]['Img_links']:
                req = requests.get(img)
                with open(f"img{count}.jpg", "w+b") as wf:
                    wf.write(req.content)
                y -= 210
                pdf_file.drawImage(f"img{count}.jpg", 300, y, width=200, height=200)

                os.remove(f"img{count}.jpg")

            y -= 30
            pdf_file.setFont('DVS', 18, leading=None)
            pdf_file.drawCentredString(415, y, news['Date'])

            y -= 30
            y = self._edit_link(pdf_file, y, news['Link'])

            y -= 30
            self._edit_text(pdf_file, y, news['Description'])

            pdf_file.showPage()

        pdf_file.save()

    @staticmethod
    def _edit_link(pdf_file, y: int, string: str) -> int:
        if len(string) >= 80:
            link_start = string[:50]
            link_end = string[50:]

            pdf_file.setFont('DVS', 14, leading=None)
            pdf_file.drawCentredString(415, y, link_start)
            y -= 13

            pdf_file.setFont('DVS', 14, leading=None)
            pdf_file.drawCentredString(415, y, link_end)
        else:
            pdf_file.setFont('DVS', 14, leading=None)
            pdf_file.drawCentredString(415, y, string)

        return y

    @staticmethod
    def _edit_text(pdf_file, y: int, string: str) -> int:
        if len(string) >= 70:
            words = string.split(" ")
            line = ''
            for word in words:
                if len(line) < 70:
                    line = " ".join([line, word])
                    if len(line) >= 70:
                        pdf_file.setFont('DVS', 16, leading=None)
                        pdf_file.drawCentredString(415, y, line)
                        y -= 13
                        line = ''
            else:
                pdf_file.setFont('DVS', 16, leading=None)
                pdf_file.drawCentredString(415, y, line)
                y -= 13
        else:
            pdf_file.setFont('DVS', 16, leading=None)
            pdf_file.drawCentredString(415, y, string)

        return y
