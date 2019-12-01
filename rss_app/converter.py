"""
File with a class Converter designed to convert data to pdf and html formats
"""


import fpdf
from bs4 import BeautifulSoup
import os


class Converter:

    """ News conversion class """

    fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__), 'fonts', 'ttf'))

    def __init__(self, source, limit, to_pdf, to_html, log):
        self.source = source
        self.limit = limit
        self.to_pdf = to_pdf
        self.to_html = to_html
        self.log = log

    def pdf_converter(self, entries):

        """ Convert data to pdf file """

        self.log.info("Converter in pdf format")
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=14)
        for thefeedentry in entries[:self.limit]:
            path = self.get_path_image(thefeedentry)
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Title']))
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Links']['News']))
            try:
                pdf.image(path)
            except RuntimeError:
                self.log.info("Error add image")
                pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Alt image']))
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Discription']))
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Date']))
            pdf.ln(10)
        pdf.output(self.to_pdf)
        print(self.to_pdf)

    def html_converter(self, entries):

        """ Convert data to html file """

        self.log.info("Converter in html format")
        with open(self.to_html, "w", encoding="utf-8") as file_text:
            file_text.write("<html>")
            file_text.write("<body>")
            file_text.write("<p>")
            for thefeedentry in entries[:self.limit]:
                file_text.write("{}<br />".format(thefeedentry['Title']))
                file_text.write("<a href = "">{}</a><br />".format(thefeedentry['Links']['News']))
                file_text.write("<img src= {} > <br />".format(thefeedentry['Links']['Image']))
                file_text.write("{} <br />".format(thefeedentry['Discription']))
                file_text.write("{} <br /><br />".format(thefeedentry['Date']))
            file_text.write("</p>")
            file_text.write("</body>")
            file_text.write("</html>")

    def get_path_image(self, thefeedentry):

        """ Get the path of the image to add to the pdf file """
        
        self.log.info("Getting path image")
        file_name_list = self.source.split("//")
        file_name = file_name_list[1].replace("/", "")
        folder_path = "image_" + file_name + os.path.sep
        if not os.path.exists(folder_path):
            self.log.info('Creating directory images')
            os.mkdir(folder_path)
        img = thefeedentry['Links']['Image']
        image = img.split("/")
        file_path = os.path.abspath('') + os.path.sep + folder_path + image[-1]
        if ".jpg" or ".gif" or ".png" in file_path:
            print(file_path)
            return file_path
        file_path += ".jpg"
        return file_path
