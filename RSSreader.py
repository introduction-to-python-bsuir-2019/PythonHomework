import feedparser
import json


class RSSreader:
    def __init__(self):
        pass

    def get_feed(self, args):
        NewsFeed = feedparser.parse(args.url)
        print(NewsFeed.entries[0].keys())
        print('Number of RSS posts:', len(NewsFeed.entries), end='\n\n')
        return NewsFeed.entries[:args.limit]

    def print_feed(self, entries):
        for entry in entries:
            print('========================================================')
            print(f'Title: {entry.title}')
            print(f'Published: {entry.published}', end='\n\n')
            print(f'Summary: {entry.summary}', end='\n\n')
            print(f'Link: {entry.link}')
            print('========================================================')

    def print_feed_json(self, entries):
        for entry in entries:
            feed = {
                'Title': entry.title,
                'Published': entry.published,
                'Summary': entry.summary,
                'Link': entry.link,
            }
            print('========================================================')
            print(json.dumps(feed, indent=2))
            print('========================================================')
