"""Module contains objects related to PDF"""
import logging
import os
from typing import Dict, Any

import requests
from fpdf import FPDF

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
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', size=18)

        self._edit_line(self.convert_data['Feed'], 18, 'C', 42, pdf)
        self._edit_line(self.convert_data['Url'], 18, 'C', 42, pdf)

        for count, entry in enumerate(self.convert_data['News']):

            self._edit_line(entry['Title'], 14, 'C', 42, pdf)

            self._edit_line(entry['Date'], 14, 'C', 42, pdf)

            pdf.cell(w=0, h=8, align="C", txt="Link on News", ln=1, link=entry['Link'])

            for img_link in entry["Links"]["Img_links"]:
                req = requests.get(img_link)
                with open(f"{count}.jpg", "w+b") as wf:
                    wf.write(req.content)

                pdf.set_x(70)
                pdf.image(f"{count}.jpg", w=70, h=70)
                os.remove(f"{count}.jpg")

            self._edit_line(entry['Description'], 16, 'C', 42, pdf)

            pdf.add_page()

        pdf.output(file_name, 'F')

    @staticmethod
    def _edit_line(txt: str, size: int, pos: str, len_l: int, pdf) -> None:

        pdf.set_font('Arial', 'B', size=size)
        split_txt = txt.split(" ")
        temp_len = 0
        line = []

        for word in split_txt:
            if temp_len + len(word) < len_l:
                line.append(word)
                temp_len += len(word)
            else:
                temp_len = 0
                line.append(word)
                pdf.cell(w=0, h=8, align=pos, txt=" ".join(line), ln=1)
                line.clear()

        if line:
            pdf.cell(w=0, h=8, align=pos, txt=" ".join(line), ln=1)
