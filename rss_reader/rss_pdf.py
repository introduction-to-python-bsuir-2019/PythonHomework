import logging
import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

styles=getSampleStyleSheet()

def save_img(url, number):
    """Downloads the image and saves it (example: image1) in the application directory"""
    logging.info("Downloading images for pdf")
    img = requests.get(url)
    file_name = "image" + str(number)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(fn, "wb") as img_file:
        img_file.write(img.content)
        img_file.close()

def remove_image(i): #TODO
    """Trying to delete downloaded for pdf images"""
    try:
        logging.info("Deleting images for pdf")
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image'+str(i))
        os.remove(fn)
    except OSError:
        pass

def prepare_string(text):
    return f'<font name="DejaVuSerif" size=12 >{text}</font>'

def to_format(text, style=styles['Normal']):
    return Paragraph(prepare_string(text), styles['Normal'])

def convert_to_pdf(news):
    """Creates pdf document in the directory which the application was launched"""
    print(80*"_")
    print("\nPlease wait while your news are packed into a pdf file right now:)")
    print(80*"_")
    pdfmetrics.registerFont(TTFont('DejaVuSerif','DejaVuSerif.ttf', 'UTF-8'))
    doc = SimpleDocTemplate("News.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    for i in range(len(news)):
        date = "Date: " + news[i].date
        if news[i].text != "" and news[i].text != " ":
            text = "Description: " + news[i].text
        feed = "Feed: " + news[i].feed
        title = "Title: " + news[i].title
        main_link = "Link: " + news[i].link
        url = news[i].url_images
        if url == [] or url[0] == '':
            url = "NO URL"
        else:
            save_img(news[i].url_images[0], i)
            file_name = "image" + str(i)
            fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
            im = Image(fn, 2*inch, 2*inch)
            Story.append(im)

        Story.append(to_format(feed))
        Story.append(Spacer(1, 12))

        Story.append(to_format(title))
        Story.append(Spacer(1, 12))

        Story.append(to_format(date))
        Story.append(Spacer(1, 12))

        Story.append(to_format(main_link))
        Story.append(Spacer(1, 12))

        Story.append(to_format(text))
        Story.append(Spacer(1, 12))

        Story.append(to_format("Other URL's: "))
        Story.append(Spacer(1, 12))
        for i in range(len(url)):
            Story.append(to_format(str(i+1) + ": " + url[i]))
    
        Story.append(PageBreak())

    doc.build(Story)
    for i in range(len(news)):
        remove_image(i)
    print(80*"_")
    print("\nSuccessfully recorded")
    print(80*"_")
    