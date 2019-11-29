import requests
import os
import logging
import base64

def save_img(url, number):
    """Downloads the image and saves it (example: _1) in the application directory"""
    logging.info("Downloading images for fb2")
    img = requests.get(url)
    file_name = "_" + str(number)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(fn, "wb") as img_file:
        img_file.write(img.content)
        img_file.close()

def remove_image(i): #TODO
    """Trying to delete downloaded for fb2 images"""
    try:
        logging.info("Deleting images for fb2")
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_'+str(i))
        os.remove(fn)
    except OSError:
        pass

def convert_to_fb2(news):
    """Creates News.fb2 document in the directory which the application was launched"""
    print(80*"_")
    print("\nPlease wait while your news are packed into a fb2 file right now:)")
    print(80*"_")
    with open("News.fb2", "w") as output:
        length = len(news)
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
        output.write("<body>\n")
        for i in range(length):
            date = "Date: " + news[i].date
            if news[i].text != "" and news[i].text != " ":
                text = "Description: " + news[i].text
                text = text.replace("&", "&amp;")
            feed = "Feed: " + news[i].feed
            feed = feed.replace("&", "&amp;")
            title = "Title: " + news[i].title
            title = title.replace("&", "&amp;")
            main_link = "Link: " + news[i].link
            main_link = main_link.replace("&", "&amp;")
            url = news[i].url_images

            output.write("\t<section>\n")
            if news[i].url_images != [''] and news[i].url_images != None and news[i].url_images != []:
                output.write('\t\t<p><image xlink:href="#_'+str(i)+'" /></p> \n')
            output.write("\t\t<title><p>"+ feed +"</p></title>\n")
            output.write("\t\t<title><p>"+ title +"</p></title><empty-line/>\n")
            output.write("\t\t<p>"+ date +"</p>\n")
            output.write("\t\t<p>"+ main_link +"</p>\n")
            output.write("\t\t<p>"+ text +"</p>\n")
            output.write("\t\t<p>Links: \n")
            for i in range(len(url)):
                output.write('\n<a>' + str(i) + ") " + url[i].replace("&", "&amp;") +'</a>\n')
            output.write("\t\t</p>\n")
            output.write("\t</section>\n")
        output.write("</body>\n")

        for i in range(length):
            url = news[i].url_images
            if news[i].url_images != [''] and news[i].url_images != None and news[i].url_images != []:
                save_img(news[i].url_images[0], i)
                file_name = "_" + str(i)
                fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
                with open (fn, "rb") as im:
                    encoded = base64.b64encode(im.read())
                    p_str = str(encoded)
                    p_str = p_str[2:len(p_str)-1]
                    output.write('<binary id="_'+str(i)+'" content-type="image/jpeg"> '+p_str+' </binary>\n')
                remove_image(i)
        output.write("</FictionBook>\n")
    print(80*"_")
    print("\nSuccessfully recorded")
    print(80*"_")
    