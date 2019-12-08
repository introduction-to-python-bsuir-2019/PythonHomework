"""This module contain class representing html utility converter """

from src.components.converter.converter_abstract import ConverterAbstract
from src.components.logger import Logger
from src.components.feed import Feed
from src.components.feed import FeedEntry
from pathlib import Path
import sys


class HtmlConverter(ConverterAbstract):
    """
        This class implements ConverterAbstract interface and convert
        rss data into html format

        Attributes:
            _log_Converter attribute contain log name converter
            _template_path attribute contain templates path
    """

    _log_Converter: str = 'HTML'
    _template_path: Path = Path(__file__).parent.joinpath('templates')

    def render(self, feed: Feed) -> str:
        """
        This method is implementation of render abstract method
        render all templates and save them into file
        :param feed: Feed
        :return:
        """
        Logger.log(
            f'Converter option choosen. Default output was declined.\n'
            f'Initialize {self._log_Converter} converter render'
        )

        self._init_template_processor(self._template_path);
        render_feeds_entries = []

        for index, entry in zip(range(self._limit), feed.entities_list):
            render_feeds_entries.append(
                self._entry_render(entry)
            )

        Logger.log('Process all render entries')

        self._save_render_file(
            self._template_processor.get_template('layout.html.jinja2').render(
                feeds_entries=render_feeds_entries,
                url=feed.feeds_url,
                logo=self._download_media(feed.feeds_image),
                title=feed.feeds_title,
                encoding=feed.feeds_encoding,
            )
        )

        Logger.log(f'{self._log_Converter} render complete. You can check it in: {self._path}')
        sys.exit(1)

    def _media_render(self, media: list) -> str:
        """
        This method is implementation of _media_render abstract method
        render media for single feed entry
        :param media: list
        :return: str
        """
        media_output = []

        for item in media:
            media_file = self._download_media(item.url)

            if not media_file:
                return self._template_processor.get_template('empty_media.html.jinja2').render()

            media_output.append(self._template_processor.get_template('media.html.jinja2').render(
                src=item.get('url', ''), alt=item.get('alt', ''))
            )

        return media_output

    def _entry_render(self, entry: FeedEntry) -> str:
        """
        This method is implementation of _entry_render abstract method
        render single feed entry
        :param entry: FeedEntry
        :return: str
        """
        return self._template_processor.get_template('entry.html.jinja2').render(
            media=self._media_render(entry.media),
            title=entry.title,
            date=entry.published,
            description=entry.description,
            link=entry.link,
            links=entry.links
        )
