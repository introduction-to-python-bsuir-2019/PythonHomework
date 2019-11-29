import fpdf
from bs4 import BeautifulSoup
import os


class Converter:
    fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__),'fonts','ttf'))  

    def __init__(self, args, log):
        self.args=args
        self.log=log

    def pdf_converter(self,entries):
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=14)
        for thefeedentry in entries:
            path = self.get_path_image(thefeedentry)            
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Title']))
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Links']['News']))
            try:
                pdf.image(path)
            except RuntimeError:
                print("Error")
                pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Alt image']))           
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Discription']))
            pdf.multi_cell(0, 10, txt="{}".format(thefeedentry['Date']))
            pdf.ln(10)
        pdf.output(self.args.to_pdf)
        print(self.args.to_pdf)
        
    def get_path_image(self, thefeedentry):
        self.log.info("Getting image name")
        file_name_list = self.args.source.split("//")
        file_name = file_name_list[1].replace("/", "")
        folder_path = "image_" + file_name + os.path.sep
        if not os.path.exists(folder_path):
            self.log.info('Creating directory images')
            os.mkdir(folder_path)        
        img = thefeedentry['Links']['Image']
        #print(img)
        image = img.split("/")
        file_path = os.path.abspath('') + os.path.sep + folder_path + image[-1]
        if ".jpg" or ".gif" or ".png" in file_path:
            return file_path
        file_path += ".jpg"
        return file_path