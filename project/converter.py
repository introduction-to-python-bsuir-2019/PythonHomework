from .log_helper import stdout_write, write_progressbar
from random import randint
from time import time
from base64 import b64encode
import os
import urllib.request
import urllib.error


class Converter():
    """Converter class. Convert data to some format"""

    def to_json(self, feed, column, verbose):
        """Take data and return it in json"""
        stdout_write("Convert to json...", verbose=verbose)
        counter = 0
        if verbose:
            write_progressbar(len(column), counter)
        json_text = '{\n  "title": "' + feed + '",\n  "news": ['
        separ = False
        for news in column:
            if separ:
                json_text += ','
            separ = True
            json_text += '{\n      "title": "' + news['title'] + '",'
            if 'date' in news:
                json_text += '\n      "date": "' + news['date'] + '",'
            json_text += '\n      "link": "' + news['link'] + '",'
            json_text += '\n      "description": "' + news['links'] + '",'
            json_text += '\n      "links": ['
            links = ""
            for lin in news['links']:
                links += f'\n        "{lin}",'
            if len(links) != 0:
                json_text += links[:-1] + "\n      ]"
            else:
                json_text += ']'
            json_text += "\n    }"
            counter += 1
            if verbose:
                write_progressbar(len(column), counter)
        json_text += ']\n}'
        return json_text

    def to_fb2(self, feed, column, url, sv_path=os.getcwd(), verbose=False):

        def next_article(id, title, images, description, feed, date="Unknown"):
            binary = []
            for img in images:
                binary += [f'<binary id="{hash(img)}.jpg" content-type="image/jpeg">{img}</binary>']
            return f"""        <section id="{id}">
            <title>
                <p>{title}</p>
            </title>
            {' '.join([f'<image l:href="#{hash(img)}.jpg"/>' for img in images])}  
            <p>{date}</p>
            <p>{description}</p>
            <p>Source: {feed}</p>
        </section>
""", binary

        def download_image(url):
            try:
                local_name, headers = urllib.request.urlretrieve(url, sv_path + url.split('/')[-1])
                stdout_write(f'Image "{url}" was downloaded.', verbose=verbose)
                return local_name
            except (urllib.error.URLError, urllib.error.HTTPError):
                stdout_write("Error occurred during downloading image")
                return ""
            except ValueError:
                stdout_write("Error: image not found")
                return ""

        fb2_begin = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
            '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"' + \
            '\n  xmlns:l="http://www.w3.org/1999/xlink">'
        fb2_end = '</FictionBook>'
        fb2_desc = f"""
    <description>
        <title-info> 
            <genre>sci_business/genre>
            <author>
                <nickname>{url}</nickname>
            </author>
            <book-title>{feed}</book-title>
            <lang>en</lang>
        </title-info>
        <document-info>
            <author>
                <nickname>{url}</nickname>
            </author>
            <date value="2011-11-11">11.11.2011</date>
            <version>3.14</version>
            <id>{hash(time()+randint(10000000, 1000000000000))}</id>
        </document-info>
    </description>
    <body>
"""
        binary = []
        fb2_text = fb2_begin + fb2_desc

        for news in column:
            image_links = []
            text_links = []
            for link in news["links"]:
                if "(image)" in link:
                    image_links += [link[:-8]]
                else:
                    text_links += [link[:-7]]
            images = []
            for link in image_links:
                img_path = download_image(link)
                try:
                    with open(img_path, 'rb') as binfile:
                        images += [b64encode(binfile.read()).decode()]
                except FileNotFoundError:
                    pass
            article, temp_bin = next_article(id=hash(hash(news["title"]) + randint(1, 10000)),
                                             title=news["title"],
                                             images=images,
                                             date=news["date"],
                                             description=news["text"] + 'links' + "\n".join(text_links),
                                             feed=feed
                                             )
            fb2_text += article
            binary += temp_bin
        binary = set(binary)
        fb2_text += "   </body>"
        for img in binary:
            fb2_text += '\n'+img+'\n'
        fb2_text += fb2_end
        file_path = f"{sv_path}/{hash(time())}-{randint(0, 100)}.fb2"
        open(file_path, 'a').close()
        with open(file_path, "w") as file:
            file.write(fb2_text)

    def to_html(self, feed, column, url, sv_path=os.getcwd(), verbose=False):
        
        def download_image(url):
            try:
                local_name, headers = urllib.request.urlretrieve(url, sv_path + url.split('/')[-1])
                stdout_write(f'Image "{url}" was downloaded.', verbose=verbose)
                return local_name
            except (urllib.error.URLError, urllib.error.HTTPError):
                stdout_write("Error occurred during downloading image")
                return ""
            except ValueError:
                stdout_write("Error: image not found")
                return ""

        def next_article(title, images, description, feed, links, date="Unknown"):
            return f"""
        <div>
            <h3>{title}</h3>
            {' '.join(f'<img src="{img}" alt="Not found">' for img in images)}
            <p>{description}</p>
            {' '.join(f'<a href="{link}">link </a>' for link in links)}
            <p>Date: {date}</p>
        </div>
            """

        def create_html(feed, main_part):
            return f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{feed}</title>
    </head>
    <body>
{main_part}
    </body>
</html>
"""

        html_text = ""
        for news in column:
            image_links = []
            text_links = []
            for link in news["links"]:
                if "(image)" in link:
                    image_links += [link[:-8]]
                else:
                    text_links += [link[:-7]]
            images = []
            for link in image_links:
                img_path = download_image(link)
                images += [img_path]
                html_text += next_article(links=text_links,
                                          title=news["title"],
                                          images=images,
                                          date=news["date"],
                                          description=news["text"],
                                          feed=feed
                                          )
        html_text = create_html(feed, html_text)        
        file_path = f"{sv_path}/{hash(time())}-{randint(0, 100)}.html"
        open(file_path, 'a').close()
        with open(file_path, "w") as file:
            file.write(html_text)
