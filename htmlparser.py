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
    def link(self, ind):
        """
        Get string line for output in links section.

        :param ind: Sequence number in the queue
        :type ind: int
        :return: string line for output in links section
        :rtype: str
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Get string line for output tag in description section.

        :return: string line for output tag in description section
        """
        pass


class A(Tag):
    """
    Class for work with tag a (link) as a class struct.
    """
    href = None

    def __str__(self):
        """
        Get string line for output tag in description section.

        :return: string line for output tag in description section
        """
        return "[link %d]"

    def link(self, ind):
        """
        Get string line for output in links section.

        :param ind: Sequence number in the queue
        :type ind: int
        :return: string line for output in links section
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
        Get string line for output tag in description section.

        :return: string line for output tag in description section
        """
        return f"[Image %d: {self.alt or 'None'}] "

    def link(self, ind):
        """
        Get string line for output in links section.

        :param ind: Sequence number in the queue
        :type ind: int
        :return: string line for output in links section
        :rtype: str
        """
        return "[%d]: %s (image)" % (ind, self.src)


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

    def get_json(self, articles, title):
        """
        Method for converting given articles and title of RSS Source to JSON format.

        :param articles: articles for convert to JSON format
        :param title: title of RSS Source
        :return: JSON format of given articles with title of RSS Source
        :rtype: str
        """
        result = {
            'title': title['feed'],
            'articles': {
                str(i): self._article_to_dict(articles[i]) for i in range(len(articles))
            }
        }
        return dumps(result)

    def parse_article(self, article):
        """
        Method for converting article to dict with given article info in specified format
        :param article: article for converting to dict in specified format
        :type article: dict
        :return: dict with article info in specified format
        """
        description, links = self._process_text(article.description, True)
        return {'title': article.title,
                'description': description,
                'link': article.link,
                'pubDate': article.published
                }, links

    @staticmethod
    def _get_next_tag(line):
        """
        Method for getting startpos and endpos of tag in given string line
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

        :param params: info for creating tag.
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

    def _parse_params_from_line(self, tag_line):
        """
        Method for getting all parameters from html tag string line.
        If parameter have a value params save value. Else value is True.

        :param tag_line: line with tag parameters.
        :type tag_line: str
        :return: dict with parsed parameters.
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

        :param tag_line: line with tag info and strings.
        :type tag_line: str
        :return: tuple (strings, tag_line).
            strings is a list with all cutting strings.
            tag_line is a given string parameter without cutting strings.
        :rtype: tuple
        """
        strings = []
        while (start_ind := tag_line.find('"')) != -1:
            end_ind = tag_line.find('"', start_ind + 1) + 1
            strings.append(tag_line[start_ind + 1: end_ind - 1])
            tag_line = tag_line[:start_ind] + tag_line[end_ind:]
        return strings, tag_line

    def _get_desc_only(self, line):
        """
        Method for getting description on news article without inserts links.

        :param line: description with tags and useless links
        :type line: str
        :return: description on news article without useless info. Text description only
        :rtype: str
        """
        description, _ = self._process_text(line, False)
        return description

    def _get_images_from_article(self, article):
        """
        Method for parsing info about all images in given article.

        :param article: article for parse info about all images
        :type article: dict
        :return: list of tag Image objects info about images
        :rtype: list
        """
        if self._stack is []:
            self._process_text(article.description, False)
        return [obj for obj in self._stack if isinstance(obj, Img)]

    def _process_text(self, description, fill_desc):
        """
        Method processing

        :param description: description of news article with useless info and tags
        :param fill_desc: adding formatted links in description or not
        :type description: str
        :type fill_desc: True
        :return: tuple (description, links)
            description is description without useless info and tags. With inserts links or not
            links is list with formatted strings with links from all created tag objects
        :rtype: tuple
        """
        self._stack.clear()
        index_of_tag = 1
        links = []
        while (pos_tag := self._get_next_tag(description)) is not None:
            first_quotes, last_quotes = pos_tag
            full_tag_line = description[first_quotes: last_quotes]
            parameters = self._parse_params_from_line(full_tag_line)
            obj_tag = self._create_tag(parameters)
            if obj_tag is not None:
                self._stack.append(obj_tag)
                if fill_desc:
                    description = description[:first_quotes] + (str(obj_tag) % index_of_tag) + description[last_quotes:]
                else:
                    description = description[:first_quotes] + description[last_quotes:]
                links.append(obj_tag.link(index_of_tag))
                index_of_tag += 1
            else:
                description = description[:first_quotes] + description[last_quotes:]

        return description, links

    def _article_to_dict(self, article):
        """
        Method for converting article info into dict of specific format.

        :param article: article for converting into dict of specific format
        :type article: dict
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

        result = {'title': article.title,
                  'description': self._get_desc_only(article.description),
                  'link': article.link,
                  'pubDate': article.published,
                  'media': images_from_article_to_dict(article)
                  }

        return result


Parser = HTMLParser()
