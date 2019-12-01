import json
from fabulous import image, color
from fabulous.text import Text
from datetime import time, datetime


class FeedFormatter:

    is_json = False

    @classmethod
    def generate_output(cls, feeds, limit, top_data_output, is_colorize=False):

        if not cls.is_json:
            return cls._default_output(feeds, limit, top_data_output, is_colorize)

        return cls._json_output(feeds, limit, top_data_output)

    @classmethod
    def _default_output(cls, feeds, limit, top_data_output, is_colorize):

        if is_colorize:
            print(Text("Console Rss Reader!", fsize=19, color='#f44a41', shadow=False, skew=4))
            formatted_feeds = ''.join(cls._colorize_single_feed_format_default(feed) for feed in feeds[:limit])
        else:
            formatted_feeds = ''.join(cls._single_feed_format_default(feed) for feed in feeds[:limit])

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
    def _json_output(cls, feeds, limit, top_data_output):
        formatted_feeds = ',\n'.join(cls._single_feed_format_json(feed) for feed in feeds[:limit])

        #tmp
        output =  json.dumps({
            "title" : top_data_output.title,
            "items" : formatted_feeds
        }, indent=4, sort_keys=True)

        return formatted_feeds

    @classmethod
    def _single_feed_format_default(cls,feed):
        return f'\
            \r{cls._delimiter()}\n\n\
            \rTitle: {feed.title}\n\
            \rDate: {cls.human_date(feed.published)}\n\
            \rLink:{feed.link}\n\n\
            \r{feed.description}\n\n\
            \rMedia: {cls.format_media(feed.media)}\n\
            \rLinks: {cls.format_links(feed.links)}\n'

    @classmethod
    def _colorize_single_feed_format_default(cls, feed):
        return f'\
            \r{color.highlight_red(cls._delimiter())}\n\n\
            \r{color.italic(color.magenta("Title"))}: {color.highlight_magenta(feed.title)}\n\
            \r{color.bold(color.yellow("Date"))}: {color.highlight_yellow(cls.human_date(feed.published))}\n\
            \r{color.bold(color.blue("Link"))}: {color.highlight_blue(feed.link)}\n\n\
            \r{color.highlight_green(feed.description)}\n\n\
            \r{color.bold(color.blue("Media"))}: {color.bold(cls.format_media(feed.media))}\n\
            \r{color.bold(color.blue("Links"))}: {color.bold(cls.format_links(feed.links))}\n'

    @classmethod
    def _single_feed_format_json(cls, feed):
        return json.dumps({
            "item": {
                "link": feed.link,
                "body": {
                     "title": feed.title,
                     "date": cls.human_date(feed.published),
                     "links": cls.format_links(feed.links),
                     "description": feed.description
                }
            }
        }, indent=4)


    @staticmethod
    def format_links(links: list) -> str:

        if not links:
            return '———— No data ————'

        def formatted(link, count):
            return f'[{count}] {link["href"]} ({link["type"]})\n'

        return ''.join(
            formatted(link, count) for count, link in enumerate(links, start=1)
        )

    @staticmethod
    def format_media(media: list) -> str:

        if not media:
            return '———— No data ————'

        def formatted(media):
            return f' {media["url"]}\n'

        return ''.join(formatted(item) for item in media)

    @staticmethod
    def human_date(date):
        if isinstance(date, type('str')):
            return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        return date.strftime("%a, %d %b %Y %H:%M:%S %z")

    @staticmethod
    def _delimiter():
        return ''.join('#' * 100)

    @staticmethod
    def _delimiter_seondary():
        return ''.join('—' * 50)
