import os
from app.rssConverter.ImageDownloader import ImageDownloader
from app.rssConverter.Exeptions import IncorrectAddress


class HtmlConverter:
    """Class for converting in html format"""

    def __init__(self, image_dir, news):
        self.html_template = '<h2>{title}</h2> <a href= {link} >Full news link</a>' \
                             '<p>Description:{description} </p><img src="data:image/png;base64, {image} "alt="" ' \
                             'width=120 height=100 border=2><p>PublicationDate: {pub_date} </p> '
        self.html_start = '<!DOCTYPE html><html><body>'
        self.html_end = '</body></html>'
        self.image_dir = image_dir
        self.news = news
        self.file_name = None

    def create_html_file(self, address):
        """html file creation"""
        try:
            self.file_name = os.path.join(address, "news.html")
        except Exception:
            raise IncorrectAddress(address)

    def parse_news(self):
        """Writing news to html file"""
        with open(self.file_name, "w") as f:
            f.write(self.html_start)
            for new in self.news:
                image = ImageDownloader.get_image(new.items['images'], self.image_dir)
                if new.items['pubDate'] == 'Unknown':
                    pub_date = new.items['published']
                else:
                    pub_date = new.items['pubDate']
                item = self.html_template.format(title=new.items['title'], link=new.items['link'],
                                                 description=new.items['summary'], image=image,
                                                 pub_date=pub_date)
                f.write(item)
            f.write(self.html_end)
