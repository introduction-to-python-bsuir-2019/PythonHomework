import html
import re
import json

class News:
    """This class contains news and methods of work whit news"""
    def __init__(self, feeds_dict, limit):

        self.news = dict()
        self.all_news = list()
        self.name_of_source = feeds_dict.feed.title

        real_limit = len(feeds_dict.entries)
        if limit > 0:
            if limit < len(feeds_dict.entries):
                real_limit = limit

        for i in range(real_limit):
            self.news['title'] = html.unescape(feeds_dict.entries[i].title)
            self.news['date'] = html.unescape(feeds_dict.entries[i].published)
            self.news['link'] = html.unescape(feeds_dict.entries[i].link)
            self.news['description'] = self.clean_from_tags(html.unescape(feeds_dict.entries[i].description))

            if feeds_dict.entries[i].setdefault("media_content", None):
                media = list()
                if feeds_dict.entries[i].media_content:
                    for elem in feeds_dict.entries[i].media_content:
                        media.append({'url': elem.setdefault('url', None), 'type':elem.setdefault('type', None)})
                self.news['media'] = media.copy()

            links = list()
            if feeds_dict.entries[i].links:
                for elem in feeds_dict.entries[i].links:
                    links.append({'url': elem.setdefault('url', None), 'type': elem.setdefault('type', None)})
            self.news['links'] = links.copy()

            self.all_news.append(self.news.copy())

    @staticmethod
    def clean_from_tags(text_with_tags):
        """This function delete tags from string"""
        return re.sub('<.*?>', '', text_with_tags)

    def print(self):
        """This function print news to stdout in readable format"""
        print(f" Source: {self.name_of_source}\n")
        for elem in self.all_news:
            print("Title: ", elem['title'])
            print("Date: ", elem['date'])
            print("Link: ", elem['link'])
            print(f"Description: {elem['description']}\n")

            j = 1
            print("Links: ")
            for link in elem['links']:
                print(f'[{j}] {link["url"]} ({link["type"]})')
                j = j + 1

            if elem.setdefault('media', None):
                print("Media: ")
                for media in elem['media']:
                    print(f'[{j}] {media["url"]} ({media["type"]})')
                    j = j + 1
            print("\n")

    def to_json(self):
        """This function returns JSON-string with news"""
        return json.dumps({'Source:': self.name_of_source, 'Feeds': self.all_news}, ensure_ascii=False).encode('utf8')

