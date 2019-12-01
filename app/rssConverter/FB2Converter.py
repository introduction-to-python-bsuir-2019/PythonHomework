import os
from app.rssConverter.ImageDownloader import ImageDownloader
from datetime import datetime
from app.rssConverter.Exeptions import IncorrectAddress


class FB2Converter:
    """Class for converting in fb2 format"""

    def __init__(self, image_dir, news):
        self.fb2_template = '<body><section id="{section_id}"><title><p>{title}</p></title><p><image xlink:href="#{' \
                            'image_link}"/></p><p><emphasis>{pub_date}</emphasis></p><p>{' \
                            'description}</p><p><emphasis>{' \
                            'description}</emphasis></p><p>Source:</p></section></body><binary id="{image_link}"' \
                            'content-type="image/jpeg">{image}</binary> '
        self.fb2_start = '<?xml version="1.0" encoding="utf-8"?><FictionBook ' \
                         'xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" ' \
                         'xmlns:xlink="http://www.w3.org/1999/xlink"><description><title-info><genre>home_entertain' \
                         '</genre><book-title>news</book-title><author><last-name>RSS</last-name></author></title' \
                         '-info><document-info><date>{date}</date><id>{' \
                         'id}</id><version>1.0</version></document-info></description> '
        self.fb2_end = '</FictionBook>'
        self.image_dir = image_dir
        self.news = news
        self.file_name = None

    def create_fb2_file(self, address):
        """fb2 file creation"""
        try:
            self.file_name = os.path.join(address, "news.fb2")
        except Exception:
            raise IncorrectAddress(address)
        return self.file_name

    def parse_news(self):
        """Writing news to fb2 file"""
        with open(self.file_name, "w") as f:
            date = datetime.today().strftime('%d.%m.%Y')
            title_id = datetime.today().strftime('%d%m%Y%h%M%s')
            f.write(self.fb2_start.format(date=date, id=title_id))
            for new in enumerate(self.news):
                image = ImageDownloader.get_image(new[1].items['images'], self.image_dir)
                if new[1].items['pubDate'] == 'Unknown':
                    pub_date = new[1].items['published']
                else:
                    pub_date = new[1].items['pubDate']
                image_link = "_" + str(new[0]) + ".jpg"
                item = self.fb2_template.format(section_id=str(new[0]), title=new[1].items['title'],
                                                link=new[1].items['link'], image_link=image_link,
                                                description=new[1].items['summary'], image=image,
                                                pub_date=pub_date)
                f.write(item)
            f.write(self.fb2_end)
