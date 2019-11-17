
class FeedFormatter:

    @classmethod
    def generate_output(cls, feeds, limit, is_json=False):
        if not is_json:
            return ''.join(cls._single_feed_format(feed) for feed in feeds[:limit])

        return Exception('json is not implemented')

    @classmethod
    def _single_feed_format(self,feed):
        return f'\
            \rTitle: {feed.title}\n\
            \rDate: {feed.date}\n\
            \rLink: {feed.link}\n\n\
            \r{feed.description}\n\n\
            \rLinks:\n\r{feed.links}\n\n'
