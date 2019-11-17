from abc import ABC, abstractmethod
from json import dumps

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
        pass

    @abstractmethod
    def format_link(self, ind):
        """
        Get formatted link to output in the links section.

        :param ind: Sequence number in the queue
        :type ind: int
        :return: string to output in links section
        :rtype: str
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Get string to output tag in the description section.

        :return: string to output tag in the description section
        """
        pass


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
        return "[link %d]"

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
        return "[%d]: %s (link)" % (ind, self.href)


class Img(Tag):
    """
    Class for work with tag img (image) as a class struct.
    """
    src = None
    alt = None

    def __str__(self):
        """
        Get string to output tag in description section.

        :return: string to output tag in the description section
        """
        return f"[Image %d: {self.alt or 'None'}] "

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
        return "[%d]: %s (image)" % (ind, self.src)


class Article:
    """
    News feed object oriented model. Use for work with articles like a class.
    """
    def __init__(self):
        self.title = None
        self.description = None
        self.link = None
        self.pubDate = None
        self.media = None
        self.links = None

    @classmethod
    def from_dict(cls, fields: dict):
        """
        An alternative constructor for creating an article model from the dict of the parsed article.

        :param fields: dict with all needed fields for current article
        :type fields: dict
        :return: article object with needed data in fields
        :rtype: Article
        """
        obj = cls()
        for f, v in fields.items():
            setattr(obj, f, v)

        return obj

    def to_dict(self, fields=None):
        """
        Method for getting a dictionary with all fields of self object.
        You can customize fields by giving a list with needing you fields.

        :param fields: optional parameter to change the content of returned dict
        :return: dict with all fields
        """
        if fields is None:
            _fields = (
                'title',
                'description',
                'link',
                'pubDate',
                'media',
                'links',
            )
        else:
            _fields = fields

        return {f: getattr(self, f, None) for f in _fields}


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
        self._stack = []

    def get_json(self, response, limit):
        """
        Method for converting given articles and title of RSS Source to JSON format.

        :param response: response struct for parse
        :param limit: required number of articles to show
        :type response: dict
        :type limit: int
        :return: JSON format of given articles with title of RSS Source
        :rtype: str
        """
        title, articles = self.parse_all(response, limit, False, False)

        result = {
            'title': title['feed'],
            'articles': {
                i: articles[i].to_dict(None) for i in range(len(articles))
            }
        }
        return dumps(result)

    def parse_all(self, response, limit, fill_desc=True, nice_links=True):
        """
        A method of parsing news articles and creating object models for easy access.

        :param response: response struct for parse
        :param limit: required number of articles to show
        :param fill_desc: adding formatted links in description or not
        :param nice_links: return formatted links or not
        :type response: dict
        :type limit: int
        :type fill_desc: bool
        :type nice_links: bool
        :return: return a tuple (title, articles).
            Title is header of RSS Source.
            Articles is a list of object of type Article was created from parsed feeds
        :rtype: tuple
        """
        raw_articles = self._get_limited_articles(response, limit)
        nice_articles = [self._article_to_dict(article, fill_desc, nice_links) for article in raw_articles]
        articles = [Article.from_dict(article) for article in nice_articles]
        title = self._get_title(response)
        return title, articles

    @staticmethod
    def _get_title(response):
        """
        Static method for parsing header of RSS Source.

        :param response: response struct for parse
        :type response: dict
        :return: header of RSS Source if parsing was successful, else None
        :rtype: dict or None
        """
        try:
            return {'feed': response.feed.title}
        except KeyError:
            return None

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
            return result[0:min(limit, len(result))]
        else:
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

    def _get_images_from_article(self, article):
        """
        Method for parsing info about all images in given article.

        :param article: article for parse info about all images
        :type article: dict
        :return: list of tag Image objects info about images
        :rtype: list
        """
        if self._stack is []:
            self._process_description(article.description, False, False)
        return [obj for obj in self._stack if isinstance(obj, Img)]

    def _process_description(self, description, fill_desc, nice_links):
        """
        Method processing description. Use flags to control result.
        Flag `fill_desc` adding formatted links in description.
        Flag `nice_links` return formatted links.

        :param description: description of news article with useless info and tags
        :param fill_desc: adding formatted links in description or not
        :param nice_links: return formatted links or not
        :type description: str
        :type fill_desc: bool
        :type nice_links: bool
        :return: tuple (description, links).
            description is description without useless info and tags. With inserts links or not.
            links is list with formatted strings with links from all created tag objects
        :rtype: tuple
        """
        self._stack.clear()
        index_of_tag = 1
        links = []
        while (pos_tag := self._get_next_tag(description)) is not None:
            first_quotes, last_quotes = pos_tag
            full_tag_line = description[first_quotes: last_quotes]
            parameters = self._get_params_from_line(full_tag_line)
            obj_tag = self._create_tag(parameters)
            if obj_tag is not None:
                self._stack.append(obj_tag)
                if fill_desc:
                    description = description[:first_quotes] + (str(obj_tag) % index_of_tag) + description[last_quotes:]
                else:
                    description = description[:first_quotes] + description[last_quotes:]

                if nice_links:
                    links.append(obj_tag.format_link(index_of_tag))
                else:
                    links.append(obj_tag.link())

                index_of_tag += 1
            else:
                description = description[:first_quotes] + description[last_quotes:]

        return description, links

    def _article_to_dict(self, article, fill_desc, nice_links):
        """
        Method for converting article info into dict of specific format.

        :param article: article for converting into dict of specific format
        :param fill_desc: adding formatted links in description or not
        :param nice_links: return formatted links or not
        :type article: dict
        :type fill_desc: bool
        :type nice_links: bool
        :return: dict of specific format
        :rtype: dict
        """

        def images_from_article_to_dict(art):
            content = self._get_images_from_article(art)
            return {
                str(i): {
                    'src': content[i].src,
                    'alt': content[i].alt
                } for i in range(len(content))
            }

        description, links = self._process_description(article.description, fill_desc, nice_links)

        result = {
            'title': article.title,
            'description': description,
            'link': article.link,
            'pubDate': article.published,
            'media': images_from_article_to_dict(article),
            'links': links,
        }

        return result


Parser = HTMLParser()
