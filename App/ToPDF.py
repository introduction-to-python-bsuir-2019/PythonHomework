import weasyprint
import logging


class ToPDF:
    """Class responsible for converting data to pdf"""
    def __init__(self, html, path="./news.pdf"):
        self.html = html
        self.path = path
        self.pdf = self.make_pdf()

    def make_pdf(self):
        """Create pdf"""
        logging.info("Creating pdf")
        return weasyprint.HTML(string=self.html).write_pdf()

    def make_file(self):
        """Create pdf file"""
        logging.info("Creating pdf file")
        try:
            with open(self.path, "wb") as f:
                f.write(self.pdf)
        except:
            print("Saving file error. Problems with path")
