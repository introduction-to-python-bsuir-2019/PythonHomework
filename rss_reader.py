import feedparser
import html

import argparse

__version__ = '0.1'


class RSSReader:
    def execute(self, source, verbose, limit, as_json):
        response = feedparser.parse(source)
        title = self._parse_title_(response)
        articles = self._parse_articles_(response, limit)

        self.print_all_articles(articles, feed=title)

    def print_all_articles(self, articles, feed=None):
        if feed is not None:
            print(f"Feed: {feed['feed']}\n")

        for article in articles:
            self.print_article(article)
            print('--------------------------------------------------')

    def print_article(self, article):
        description, links = self.get_description_and_links(article)
        print(f"Title: {article.title}\n"
              f"Date: {article.published}\n"
              f"Link: {article.link}\n\n"
              f"{description}\n\n"
              f"Links:")
        for link in links:
            print(link)

    @staticmethod
    def delete_all_tags(text: str, tag):
        start_ind = text.find(f'<{tag}')
        while start_ind != -1:
            end_ind = text.find(f'{tag}>')
            text = text[:start_ind:] + text[end_ind + 1:]
            start_ind = text.find(f'<{tag}')
        return text

    @staticmethod
    def get_description_and_links(article):
        description = html.unescape(article.description)
        images = []
        links = []
        i = 0
        ind = 1
        if (i := article.description.find('href="', i)) != -1:
            str_url = article.description[i + 6: article.description.find('"', i + 7)]
            links.append(f"[{ind}]: {str_url}")

        while (i := article.description.find('<img', i)) != -1:
            img_start = i
            ind += 1
            i += 1
            desc_image = ''
            if (i := article.description.find('alt="', i)) != -1:
                start_ind = i + 5
                end_ind = article.description.find('"', i + 6)
                str_alt = html.unescape(article.description[start_ind: end_ind])
                if not str_alt.isspace():
                    desc_image += f"[image {ind}: {str_alt}]"
            desc_image += f"[{ind}]"
            images.append(desc_image)
            img_end = article.description.find('>', i + 2) + 1
            description = description[:img_start] + description[img_end:]

        ind = 2
        for media in article.media_content:
            links.append(f"[{ind}]: {media['url']}")
            ind += 1
        return description, links

    @staticmethod
    def _parse_title_(response):
        try:
            return {'feed': response['feed']['title']}
        except KeyError:
            return None

    @staticmethod
    def _parse_articles_(response, limit):
        result = response.entries
        if limit is not None:
            return result[0:min(limit, len(result))]
        else:
            return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', action='store', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    settings = parser.parse_args()

    if settings.version:
        print(__version__)

    RSSReader().execute("https://news.yahoo.com/rss/", settings.verbose, settings.limit, settings.json)


if __name__ == '__main__':
    main()
