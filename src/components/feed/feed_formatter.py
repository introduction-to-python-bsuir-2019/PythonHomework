import json
from fabulous import image, color
from fabulous.text import Text


class FeedFormatter:

    is_json = False

    @classmethod
    def generate_output(cls, feeds, limit, title, is_colorize=False):

        if not cls.is_json:
            return cls._default_output(feeds, limit, title, is_colorize)

        return cls._json_output(feeds, limit, title)

    @classmethod
    def _default_output(cls, feeds, limit, title, is_colorize):

        if is_colorize:
            print(Text("Console Rss Reader!", fsize=19, color='#f44a41', shadow=False, skew=4))
            formatted_feeds = ''.join(cls._colorize_single_feed_format_default(feed) for feed in feeds[:limit])
        else:
            formatted_feeds = ''.join(cls._single_feed_format_default(feed) for feed in feeds[:limit])

        return 'Feed: {0}\n\n{1}'.format(title, formatted_feeds)

    @classmethod
    def _json_output(cls, feeds, limit, title):
        formatted_feeds = ',\n'.join(cls._single_feed_format_json(feed) for feed in feeds[:limit])

        #tmp
        output =  json.dumps({
            "title" : title,
            "items" : formatted_feeds
        }, indent=4, sort_keys=True)

        return formatted_feeds

    @classmethod
    def _single_feed_format_default(self,feed):
        return f'\
            \r{self._delimiter()}\n\n\
            \rTitle: {feed.title}\n\
            \rDate: {feed.date}\n\
            \rLink: {feed.link}\n\n\
            \r{feed.description}\n\n\
            \rLinks:\n\r{feed.links}\n'

    @classmethod
    def _colorize_single_feed_format_default(self, feed):
        return f'\
            \r{color.highlight_red(self._delimiter())}\n\n\
            \r{color.italic(color.magenta("Title"))}: {color.highlight_magenta(feed.title)}\n\
            \r{color.bold(color.yellow("Date"))}: {color.highlight_yellow(feed.date)}\n\
            \r{color.bold(color.blue("Link"))}: {color.highlight_blue(feed.link)}\n\n\
            \r{color.highlight_green(feed.description)}\n\n\
            \r{color.bold("Links")}:\n\r{color.bold(feed.links)}\n'


    @classmethod
    def _single_feed_format_json(cls, feed):
        return json.dumps({
            "item": {
                "link": feed.link,
                "body": {
                     "title": feed.title,
                     "date": feed.date,
                     "links": feed.links,
                     "description": feed.description
                }
            }
        }, indent=4)

    @staticmethod
    def _delimiter():
        return ''.join('#' * 100)
