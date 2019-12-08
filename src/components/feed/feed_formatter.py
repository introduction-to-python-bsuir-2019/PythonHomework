"""this module contain class for various formatter output parsing data in console """

import json
from fabulous import color
from fabulous.text import Text
from datetime import datetime
from src.components.helper import Map


class FeedFormatter:
    """
        This class provide a way for formatting data into console depending on the selected options
        Attributes:
            is_json store state of output case
    """

    is_json = False

    @classmethod
    def generate_output(cls, entries: list, limit: int, top_data_output: Map, is_colorize: bool=False) -> str:
        """
        This method decide which way rss feed should be printed
        :param entries: list
        :param limit: int
        :param top_data_output: Map
        :param is_colorize: bool
        :return:
        """
        if not cls.is_json:
            return cls._default_output(entries, limit, top_data_output, is_colorize)

        return cls._json_output(entries, limit, top_data_output)

    @classmethod
    def _default_output(cls, entries: list, limit: int, top_data_output: Map, is_colorize) -> str:
        """
        This method render data for default output case
        :param entries: list
        :param limit: int
        :param top_data_output: Map
        :param is_colorize: bool
        :return:
        """
        if is_colorize:
            print(Text("Console Rss Reader!", fsize=19, color='#f44a41', shadow=False, skew=4))

            formatted_feeds = ''.join(cls._colorize_single_feed_format_default(feed) for feed in entries[:limit])
        else:
            formatted_feeds = ''.join(cls._single_feed_format_default(feed) for feed in entries[:limit])

        if is_colorize:
            return 'Feed: {0}\nUrl: {1}\n\n{2}'.format(
                color.highlight_black(top_data_output.title),
                color.highlight_red(top_data_output.url),
                formatted_feeds
            )

        return 'Feed: {0}\nUrl: {1}\n\n{2}'.format(
            f'——— {top_data_output.title} ———',
            f'——— {top_data_output.url} ———',
            formatted_feeds
        )

    @classmethod
    def _json_output(cls, entries: list, limit: int, top_data_output: Map) -> str:
        """
        This method render data for json output case
        :param entries: list
        :param limit: int
        :param top_data_output: Map
        :return:
        """
        formatted_feeds = [cls._single_feed_format_json(feed) for feed in entries[:limit]]

        output = json.dumps({
            "title": top_data_output.title,
            "url": top_data_output.url,
            "image": top_data_output.image,
            "entries" : formatted_feeds,
        }, indent=2, sort_keys=False, ensure_ascii=False)

        return output.encode(top_data_output.encoding).decode()

    @classmethod
    def _single_feed_format_default(cls, entry: object) ->str:
        """
        This method render single entry for default output
        :param entry: object
        :return: str
        """
        return f'\
            \r{cls._delimiter()}\n\n\
            \rTitle: {entry.title}\n\
            \rDate: {cls.human_date(entry.published)}\n\
            \rLink:{entry.link}\n\n\
            \r{entry.description}\n\n\
            \rMedia: {cls.format_media(entry.media)}\n\
            \rLinks: {cls.format_links(entry.links)}\n'

    @classmethod
    def _colorize_single_feed_format_default(cls, entry: object) -> str:
        """
        This method render single entry for default output with colorizee option
        :param entry: object
        :return: str
        """
        return f'\
            \r{color.highlight_red(cls._delimiter())}\n\n\
            \r{color.italic(color.magenta("Title"))}: {color.highlight_magenta(entry.title)}\n\
            \r{color.bold(color.yellow("Date"))}: {color.highlight_yellow(cls.human_date(entry.published))}\n\
            \r{color.bold(color.blue("Link"))}: {color.highlight_blue(entry.link)}\n\n\
            \r{color.highlight_green(entry.description)}\n\n\
            \r{color.bold(color.blue("Media"))}: {color.bold(cls.format_media(entry.media))}\n\
            \r{color.bold(color.blue("Links"))}: {color.bold(cls.format_links(entry.links))}\n'

    @classmethod
    def _single_feed_format_json(cls, entry: object) -> str:
        """
        This method render single entry for json output
        :param entry: object
        :return: str
        """
        return {
            "entry": {
                "link": entry.link,
                "body": {
                     "title": entry.title,
                     "date": str(cls.human_date(entry.published)),
                     "links": [{
                         'href':link.href,
                         'type': link.type,
                     } for link in entry.links],
                     "media": [{
                         'url':media.url,
                         'additional': media.additional,
                     } for media in entry.media],
                     "description": entry.description
                }
            }
        }

    @staticmethod
    def format_links(links: list) -> str:
        """
        This static method beautifying provided links
        :param entry: object
        :return: str
        """
        if not links:
            return '———— No data ————'

        def formatted(link, count):
            return f'[{count}] {link["href"]} ({link["type"]})\n'

        return ''.join(
            formatted(link, count) for count, link in enumerate(links, start=1)
        )

    @staticmethod
    def format_media(media: list) -> str:
        """
        This static method beautifying provided media urls
        :param media:list
        :return: str
        """

        if not media:
            return '———— No data ————'

        def formatted(media):
            return f' {media["url"]}\n'

        return ''.join(formatted(item) for item in media)

    @staticmethod
    def human_date(date) -> datetime:
        """
        This static method provide more readable for human date format
        :param date:
        :return: datetime
        """
        if isinstance(date, type('str')):
            return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        return date.strftime("%a, %d %b %Y - [%H:%M:%S]")

    @staticmethod
    def _delimiter() -> str:
        """
        This static method provide simple delimiter between feeds entries
        :return: str
        """
        return ''.join('#' * 100)

    @staticmethod
    def _delimiter_secondary() -> str:
        """
        This static method provide  second variant of simple delimiter between feeds entries
        :return: str
        """
        return ''.join('—' * 50)
