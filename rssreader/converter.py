import logging
import time
from typing import List, Dict, Tuple
from hashlib import md5
from pathlib import Path
import urllib
from base64 import b64encode
import shutil
import html
from abc import ABC, abstractmethod

from rssreader import conf
from rssreader.base import BaseClass


class Converter(ABC):
    """Basic class for any converter"""
    def __init__(self, cache_dir: Path, file_path: Path) -> None:
        """Constructor. Additionally create a file directory and init cache image directory (if necessary)."""
        self.file_path = file_path
        self.cache_dir = cache_dir
        self._init_file_dir()
        self._init_image_dir(cache_dir)

    def _init_file_dir(self) -> None:
        """Create a directory (if necessary) where converting file will be saved"""
        if self.file_path.parent.exists():
            logging.info(f'Directory "{self.file_path.parent}" already exists')
        else:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            logging.info(f'Directory "{self.file_path.parent}" has been created')

    def _init_image_dir(self, cache_dir: Path) -> None:
        """Create a directory (if missed) to store downloaded images"""
        self.image_dir = cache_dir.joinpath('images')
        if self.image_dir.exists():
            logging.info(f'Directory "{self.image_dir}" to store images already exists')
        else:
            self.image_dir.mkdir(parents=True, exist_ok=True)
            logging.info(f'Directory "{self.image_dir}" to store images has been created')

        self._default_image = {'name': 'no_image.jpg', 'type': 'image/jpeg', 'url': ''}

        # check whether default image is missed in image cache
        image_cache_path = self.image_dir.joinpath(self._default_image['name'])
        if not image_cache_path.exists():
            image_source_path = Path(__file__).parent.joinpath('data', self._default_image['name'])
            if image_source_path.exists():
                shutil.copyfile(image_source_path, image_cache_path)
                logging.info('Default image is copied into image cache folder')
            else:
                raise FileNotFoundError(f'Default image "{image_source_path}" does not exist.')

        self._default_image['data'] = self._get_image_binary(image_cache_path)

    @staticmethod
    def _get_image_binary(image_path: Path) -> str:
        """Return image base64 binary as string"""
        with open(image_path, 'rb') as f:
            return b64encode(f.read()).decode()

    @staticmethod
    def _obtain_image_ident(url: str) -> str:
        """Return image identifier to be used in image cache instead of a real long name"""
        return md5(url.encode()).hexdigest() + Path(url).suffix

    @staticmethod
    def _download_image(url: str, image_path: Path) -> bool:
        """Download an image. If it is finished successfully returns True. Otherwise, false."""
        try:
            urllib.request.urlretrieve(url, image_path)
            logging.info(f'Image "{url}" was downloaded.')
            return True
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            logging.info(f'An error occurred during downloading image "{url}". Details are "{e}"')
            return False

    @abstractmethod
    def _convert(self, feed: "rssreader.feed.Feed") -> str:
        """Return result of news converting"""

    def _save(self, data: str) -> None:
        with open(str(self.file_path), 'w') as file:
            file.write(data)
            logging.info(f'File has been saved in "{self.file_path}"')

    def perform(self, feed: "rssreader.feed.Feed") -> None:
        """Perform converting"""
        start = time.time()
        self._save(self._convert(feed))
        logging.info(f'Converting has taken {round((time.time() - start), 4)}s')


class HTMLConverter(BaseClass, Converter):
    """Class is used to convert news into HTML format"""
    def __init__(self, cache_dir: Path, file_path: Path) -> None:
        """Constructor. Additionally define all templates"""
        super().__init__(cache_dir, file_path)

        self.book_template = '''\
<html>
  <head>
    <meta charset="{encoding}">
    <title>Offline rss</title>
  </head>
  <body>
    <center><h1>{title}</h1></center>
    {news}
  </body>
</html>'''

        self.news_template = '<h4><p>{title}</p><table><tr><td>{img}</td><td>{description}</br>' \
                             '{hrefs}</td></tr></table></h4>'''
        self.href_template = '<a href="{url}">[{i}]</a>'
        self.img_template = '<a href="{url}"><img src="data:{type};base64,{data}" ' \
                            'alt="" width=120 height=100 border=2></a>'

    def _convert(self, feed: "rssreader.feed.Feed") -> str:
        """Return result of news converting into HTML"""
        news_array = []

        logging.info('Iterate over all news:')
        for i, n in enumerate(feed.news[:feed.limit]):
            logging.info(f'[{i + 1}]: {n.link}')
            images, links = self._process_links(n.hrefs)
            news_array.append(
                self.news_template.format(
                    title=n.title, description=n.description, img=''.join(images), hrefs=''.join(links)))

        return self.book_template.format(title=feed.title, encoding=feed.encoding, news='\n    '.join(news_array))

    def _process_links(self, hrefs: List[Dict]) -> Tuple[List, List]:
        """
        Process description's links.
        Images are downloaded (if missed in cache), another links are simply added as href into the document.
        """
        images, links = [], []
        for h in hrefs:
            if h['type'].split('/')[0] == 'image':
                image_name = self._obtain_image_ident(h['href'])
                image_path = self.image_dir.joinpath(image_name)

                if image_path.exists():
                    image = {'url': h['href'], 'type': h['type'], 'data': self._get_image_binary(image_path)}
                    logging.info(f'Image {h["href"]} is loaded from cache')
                else:
                    # first of all, an image is downloaded into image cache
                    if self._download_image(h['href'], image_path):
                        image = {'url': h['href'], 'type': h['type'], 'data': self._get_image_binary(image_path)}
                    else:
                        image = {'url': h['href'], 'type': self._default_image['type'],
                                 'data': self._default_image['data']}
                        logging.info('Due to error while downloading default image is used ')

                images.append(self.img_template.format(**image))
            else:
                links.append(self.href_template.format(url=h['href'], i=len(links) + 1))

        if len(images) == 0:
            images.append(self.img_template.format(**self._default_image))
            logging.info('Default image is used because there is no image in this news')

        return images, links


class FB2Converter(BaseClass, Converter):
    """Class is used to convert news into FictionBook (v.2) format"""

    def __init__(self, cache_dir: Path, file_path: Path) -> None:
        """Constructor. Additionally define all templates"""
        super().__init__(cache_dir, file_path)

        self.book_template = '''\
<?xml version="1.0" encoding="{encoding}"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">
    <description>
        <title-info>
            <genre>home_entertain</genre>
            <book-title>{title}</book-title>
            <author><last-name>RSS</last-name>
            </author>
        </title-info>
        <document-info>
            <src-url>{url}</src-url>
            <program-used>{prog}</program-used>
            <version>1.0</version>
        </document-info>
    </description>
    <body>
      {sections}
    </body>
    {binaries}
</FictionBook>
'''
        self.news_template = '''\
<section id="news_{num}">
    <title><p>{num}. {title}</p></title>
    <p>{images}</p>
    <p>{description}</p>
    <p>More information on: {links}</p>
</section>
'''
        self.image_template = '<image l:href="#{0}"/>'
        self.binary_template = '<binary id="{name}" content-type="{type}">{data}</binary>'

    def _convert(self, feed: "rssreader.feed.Feed") -> str:
        news_array = []
        binaries = []
        self._used_images = set()  # unique set of used images to prevent from adding duplicates into binaries

        logging.info('Iterate over all news:')
        for i, n in enumerate(feed.news[:feed.limit]):
            logging.info(f'[{i + 1}]: {n.link}')
            binary, images, links = self._process_links(n.hrefs)
            news_array.append(
                self.news_template.format(num=i+1, title=html.escape(n.title), description=html.escape(n.description),
                                          images=''.join(images), links=', '.join(links)))
            binaries.extend(binary)

        return self.book_template.format(
            title=html.escape(feed.title), prog=f'{conf.__package__} {conf.__version__}', url=feed.url,
            encoding=feed.encoding, sections=''.join(news_array), binaries=''.join(binaries))

    def _process_links(self, hrefs: List[Dict]) -> Tuple[List, List, List]:
        """Process description's links"""

        binaries, images, links = [], [], []
        for h in hrefs:
            if h['type'] in ('image/jpeg', 'image/png'):  # only these types of images are supported by FictionBook
                image = {'name': self._obtain_image_ident(h['href']), 'type': h['type'], 'url': ''}
                image_path = self.image_dir.joinpath(image['name'])

                if image_path.exists():
                    logging.info(f'Image {h["href"]} is loaded from cache.')
                    images.append(self.image_template.format(image['name']))

                    if image['name'] not in self._used_images:  # an image's binary should be added only once
                        image['data'] = self._get_image_binary(image_path)
                        self._used_images.add(image['name'])
                        binaries.append(self.binary_template.format(**image))
                else:
                    if self._download_image(h['href'], image_path):
                        images.append(self.image_template.format(image['name']))
                        image['data'] = self._get_image_binary(image_path)
                        self._used_images.add(image['name'])
                        binaries.append(self.binary_template.format(**image))
                    else:
                        images.append(self.image_template.format(self._default_image['name']))
                        if self._default_image['name'] not in self._used_images:
                            self._used_images.add(self._default_image['name'])
                            binaries.append(self.binary_template.format(**self._default_image))
            else:
                links.append(h['href'])

        # it there is no image in this url, default one will be used
        if len(images) == 0:
            logging.info('Default image is used')
            images.append(self.image_template.format(self._default_image['name']))
            if self._default_image['name'] not in self._used_images:
                self._used_images.add(self._default_image['name'])
                binaries.append(self.binary_template.format(**self._default_image))

        return binaries, images, links
