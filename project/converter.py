from .log_helper import stdout_write, write_progressbar
from random import randint
from time import time
from base64 import b64encode

class Converter():
    """Converter class. Convert data to some format"""

    def to_json(feed, column, verbose):
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
        
    def to_fb2(feed, column, url, sv_path=f"/home/{str(randint(10**10))}/"):
        fb2_begin = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
        +'<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"' + \
        'xmlns:l="http://www.w3.org/1999/xlink">'
        fb2_end = '</FictionBook>'
        fb2_desc = f"""
    <description>
        <title-info> 
            <genre>news</genre>
            <author>{url}</author>
            <book-title>
                <nickname>{feed}</nickname>
            </book-title>
        </title-info>
        <document-info>
            <version>3.14159</version>
            <id>{randint(10000000, 1000000000000)}</id>
        </document-info>
    </description>
        """
        
        def next_article(id, title, images, date="Unknown", description, feed):
            return f"""
    {f'<binary id="{img}link" content-type="image/jpeg">{img}</binary>' for img in images}
    <body>
        <section id="{id}">
            <title>
                <p>{title}</p>
            </title>
            {f'<p><image l:href="#{img}link"/></p>' for img in images}  
            <p><strong>{date}</strong></p>
            <p>{description}</p>
            <p>Source:{feed}</p>
        </section>
    </body>
    """
    
        def download_image(url):
            try:
                urllib.request.urlretrieve(url, sv_path + url.split('/')[-1])
                stdout_write(f'Image "{url}" was downloaded.', verbose=verbose)
                return sv_path + url.split('/')[-1]
            except urllib.error.URLError, urllib.error.HTTPError:
                stdout_write("Error occurred during downloading image")
                return ""
    
    fb2_text = fb2_begin + fb2_desc
    for news in column:
        image_links = []
        for link in news["links"]:
            if "(image)" in link:
                image_links += [link[:-8]]
        images = []
        for link in image_links:
            img_path = download_image(link)
            with open(img_path, 'rb') as binfile:
                images += [b64encode(binfile.read()).decode()]
        fb2_text += next_article(id=hash(hash(news["title"]) + randint(1, 10000)),
                                 title=news["title"],
                                 images=images,
                                 date=news["date"],
                                 description=description+'\n'+"\n".join(links),
                                 feed=feed
        )
    fb2_text += fb2_end
    with open(f"{sv_path}{time()}-{randint(100)}.fb2", "w") as file:
        file.write(fb2_text)
