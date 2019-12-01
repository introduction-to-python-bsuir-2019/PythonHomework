"""Pdf conversion module"""
import os
import requests
import logging
from fpdf import FPDF


class PdfConversion():
    """A class that converts to Pdf"""
    def __init__(self, list_news_dict: list) -> None:
        self.list_news_dict = list_news_dict
        self.pdf = FPDF()
        self.pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.pdf.add_page()

    def __pretty_text(self, txt: str, size: int, pos: str, len_l: int) -> None:
        """
        Method that aligns text with respect
        to its length considering word breaks
        """
        self.pdf.set_font('DejaVu', '', size=size)
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
                self.pdf.cell(w=0, h=8, align=pos, txt=" ".join(line), ln=1)
                line.clear()

        if line:
            self.pdf.cell(w=0, h=8, align=pos, txt=" ".join(line), ln=1)

    def conversion_to_pdf(self):
        """Method that receives a list of news and creates pdf from it"""
        self.pdf.set_font('DejaVu', '', size=24)
        for index, news in enumerate(self.list_news_dict):
            self.__pretty_text(news["Feed"], 24, "C", 36)
            self.pdf.cell(w=0, h=20, txt=" ", ln=1)

            self.__pretty_text(news["Title"], 18, "C", 36)

            self.pdf.set_text_color(0, 0, 255)
            self.pdf.cell(
                w=0, h=8, align="C", txt="News link", ln=1, link=news["Link"])

            self.pdf.set_text_color(0, 0, 0)
            self.pdf.cell(w=0, h=15, txt=" ", ln=1)

            self.__pretty_text("Date: " + news["Date"], 14, "C", 36)

            for img in news["Links"]:
                req = requests.get(img)
                with open(f"image{index}.jpg", "w+b") as wf:
                    wf.write(req.content)
                self.pdf.set_x(70)
                try:
                    self.pdf.image(f"image{index}.jpg", w=70, h=70)
                except RuntimeError:
                    logging.debug("gif and mp4 fles are ignored")

                os.remove(f"image{index}.jpg")
            self.pdf.set_x(10)
            self.__pretty_text(news["Description"], 18, "C", 36)

            self.pdf.add_page()

        logging.info("News converted to pdf")
        logging.info("File pdf saved successfully")
        self.pdf.output("parsing_news.pdf")
