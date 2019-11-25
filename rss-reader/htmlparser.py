import logging
from abc import ABC, abstractmethod
import html

__all__ = ['Parser']


class Tag(ABC):
    """
    Abstract class for working with tags as a class structure.
    """

    def __init__(self, **kwargs):
        for arg, val in kwargs.items():
            self.__setattr__(arg, val)

    @abstractmethod
    def link(self):
        """
        Get media object source link.

        :return: media object source URL
        :rtype: str
        """

    @abstractmethod
    def format_link(self, ind):
        """
        Get formatted link to output in the links section.

        :param ind: Sequence number in the queue
        :type ind: int
        :return: string to output in links section
        :rtype: str
        """

    @abstractmethod
    def __str__(self):
        """
        Get string to output tag in the description section.

        :return: string to output tag in the description section
        """


class A(Tag):
    """
    Class for work with tag `a` (link) as a class struct.
    """
    href = None

    def __str__(self):
        """
        Get string to output tag in description section.

        :return: string to output tag in the description section
        """
        return "[link {}]"

    def link(self):
        """
        Get media object source link.

        :return: media object source URL
        :rtype: str
        """
        return self.href

    def format_link(self, ind):
        """
        Get formatted link to output in the links section.

        :param ind: Sequence number in the queue
        :type ind: int
        :return: string to output in the links section
        :rtype: str
        """
        return f"[{ind}]: {self.href} (link)"


class Img(Tag):
    """
    Class for work with tag img (image) as a class struct.
    """
    src = None
    alt = None
    width = None
    height = None

    def __str__(self):
        """
        Get string to output tag in description section.

        :return: string to output tag in the description section
        """
        return "[Image {}: {}] ".format('{}', self.alt)

    def link(self):
        """
        Get media object source link.

        :return: media object source URL
        :rtype: str
        """
        return self.src

    def format_link(self, ind):
        """
        Get formatted link to output in the links section.

        :param ind: Sequence number in the queue
        :type ind: int
        :return: string to output in the links section
        :rtype: str
        """
        return f"[{ind}]: {self.src} (image)"


class HTMLParser:
    """
    A class for parse news articles from response struct of module "feedparser".
    Methods return JSON format of news articles or dict with info about given article.
    """
    _table = {
        'a': A,
        'img': Img,
    }

    def __init__(self):
        self._tags = []

    def parse(self, response, limit):
        """
        A method of parsing news articles and creating object models for easy access.

        :param response: response struct for parse
        :param limit: required number of articles to show
        :type response: dict
        :type limit: int
        :return: return a dict {'title': str, 'articles': list).
            Title is header of RSS Source.
            Articles is a list of dicts with articles info which was created from parsed feeds
        :rtype: dict
        """
        logging.info("Getting list of limited articles")
        raw_articles = self._get_limited_articles(response, limit)

        logging.info("Completed. Converting each article to dict")
        nice_articles = [self._article_to_dict(article) for article in raw_articles]

        logging.info("Completed. Clear articles from HTML escapes")
        articles = [self._clear_from_html(article) for article in nice_articles]

        logging.info("Getting a RSS source title")
        title = response.feed.title

        return {'title': title, 'articles': articles}

    @staticmethod
    def _clear_from_html(article):
        """
        Method to clear html escapes from all fields of article.

        :param article: article to clear from HTML escapes
        :return: clean article
        """
        for k, v in article.items():
            article[k] = html.unescape(v)

        return article

    @staticmethod
    def _get_limited_articles(response, limit):
        """
        Method of limiting parsing articles from response struct.
        If limit is None return articles given length, else return all available articles.

        :param response: response struct for parse
        :param limit: limit of output news articles
        :type response: dict
        :type limit: int or None
        :return: news articles of limited length
        :rtype: dict
        """
        result = response.entries
        if limit is not None:
            logging.info(f"Completed. Loaded {min(limit, len(result))} articles with limit {limit}")
            return result[0:min(limit, len(result))]
        else:
            logging.info(f"Completed. Loaded {len(result)} articles without any limit")
            return result

    @staticmethod
    def _get_next_tag(line):
        """
        Method for getting startpos and endpos of tag in given string line.

        :param line: line with html tag
        :type line: str
        :return: (startpos, endpos) is a position of next tag in line if line have a tag, else None
        :rtype: tuple or None
        """
        if line.find('<') != -1:
            startpos = line.find('<')
            endpos = line.find('>', startpos) + 1
            return startpos, endpos
        else:
            return None

    def _create_tag(self, params):
        """
        Method for creating Tag struct class from params.

        :param params: info for creating tag
        :type params: dict
        :return: tag object if creating was successful, else None
        :rtype: Tag or None
        """
        try:
            tag_type = next(iter(params))
            params.pop(tag_type)
            return self._table[tag_type](**params)
        except KeyError:
            return None

    def _get_params_from_line(self, tag_line):
        """
        Method for getting all parameters from html tag string line.
        If parameter have a value params save value. Else value is True.

        :param tag_line: line with tag parameters
        :type tag_line: str
        :return: dict with parsed parameters
        :rtype: dict
        """
        params = {}
        tag_line = tag_line.strip('<>')
        strings, tag_line = self._get_all_strings(tag_line)
        words = tag_line.split()
        for param in words:
            pair = param.split('=')
            if len(pair) == 1:
                params.update({pair[0]: True})
            else:
                params.update({pair[0]: strings.pop(0)})

        return params

    @staticmethod
    def _get_all_strings(tag_line):
        """
        Method of cutting all string in quotes \"...\".

        :param tag_line: line with tag info and strings
        :type tag_line: str
        :return: tuple (strings, tag_line).
            strings is a list with all cutting strings.
            tag_line is a given string parameter without cutting strings
        :rtype: tuple
        """
        strings = []
        while (start_ind := tag_line.find('"')) != -1:
            end_ind = tag_line.find('"', start_ind + 1) + 1
            strings.append(tag_line[start_ind + 1: end_ind - 1])
            tag_line = tag_line[:start_ind] + tag_line[end_ind:]
        return strings, tag_line

    def _process_description(self, desc, fill_desc=True, fill_links=True):
        """
        Method processing description. Return description of specific format.

        :param desc: description of news article with useless info and tags
        :type desc: str
        :return: tuple (description, links).
            description is description without useless info and tags. With inserts links or not.
            links is list with formatted strings with links from all created tag objects
        :rtype: tuple
        """
        self._tags.clear()
        index_of_tag = 1
        links = []
        while (pos_tag := self._get_next_tag(desc)) is not None:
            first_quotes, last_quotes = pos_tag
            full_tag_line = desc[first_quotes: last_quotes]
            parameters = self._get_params_from_line(full_tag_line)
            obj_tag = self._create_tag(parameters)
            if obj_tag is not None:
                self._tags.append(obj_tag)
                if fill_desc:
                    desc = desc[:first_quotes] + str(obj_tag).format(index_of_tag) + desc[last_quotes:]
                else:
                    desc = desc[:first_quotes] + desc[last_quotes:]
                if fill_links:
                    links.append(obj_tag.format_link(index_of_tag))
                else:
                    links.append(obj_tag.link())
                index_of_tag += 1
            else:
                desc = desc[:first_quotes] + desc[last_quotes:]

        return desc, links

    def _article_to_dict(self, article):
        """
        Method for converting article info into dict of specific format.

        :param article: article for converting into dict of specific format
        :type article: dict
        :return: dict of specific format
        :rtype: dict
        """

        dec_description, dec_links = self._process_description(article.description)
        description, links = self._process_description(article.description, False, False)

        images = [obj for obj in self._tags if isinstance(obj, Img)]

        media = [
            {"src": image.src,
             "alt": image.alt,
             "width": image.width,
             "height": image.height} for image in images
        ]

        result = {
            'title': article.title,
            'description': description,
            'dec_description': dec_description,
            'link': article.link,
            'pubDate': article.published,
            'media': media,
            'links': links,
            'dec_links': dec_links,
        }

        return result


Parser = HTMLParser()
