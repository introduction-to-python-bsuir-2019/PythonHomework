import json
from logging import Logger
from typing import List, Optional
from xml.etree import ElementTree

from .article import Article
from .logger import default_logger


class Document:
    """
    Represents the RSS document data.
    """

    @classmethod
    def from_xml(
        cls, document: ElementTree.Element, limit: Optional[int] = 0, logger: Optional[Logger] = default_logger
    ):
        """
        Constructs new RSS Document from an XML element.

        Params:
            - document (ElementTree.Element): XML element to parse the document from
            - limit (Optional[int]): Maximum amount of articles to parse (defaults to 0, which means "all articles")
            - logger (Logger): Logger instance to use for logging inside the class

        Returns:
            - Document class instance which contains the parsed data
        """

        # Grab the `channel` element from RSS document (it contains all the required content)
        channel = document.find("channel")
        logger.info("Got document channel element: %s", str(channel))

        # Grab the whole blog title (it is usually first `title` element in RSS documents)
        feed = channel.find("title")
        logger.info("Got document title element: %s", feed.text)

        # Grab all articles items
        all_items = channel.findall("item")
        logger.info("Got %d articles elements", len(all_items))

        # Use provided limit value to limit the articles iterations
        end_of_parsing = limit if limit else len(all_items)
        logger.info("Parsing document articles until reaching the limit: %d", end_of_parsing)

        # Construct articles from the RSS document
        articles = []
        for item in all_items[:end_of_parsing]:
            articles.append(Article.from_xml(item, logger))

        return cls(feed.text, articles, logger)

    def __init__(self, feed: str, articles: List[Article], logger: Logger):
        """
        Constructs new Document from parsed data.

        It is not recommended to call this method direclty with parsed XML, instead use `Document.from_xml` class method.

        Params:
            - feed (str): The main blog title
            - articles (List[Article]): The parsed blog articles list
            - logger (Logger): Logger instance to use for logging inside the class

        Returns:
            - The constructed Document object
        """

        self.feed = feed
        self.articles = articles
        self.logger = logger

    def to_string(self) -> str:
        """
        Returns string representation of a Document.
        """

        self.logger.info("Converting document header to string")

        feed = f"\nFeed: {self.feed}\n\n"
        articles = ""

        self.logger.info("Converting document articles to string")

        for a in self.articles:
            articles += "=" * 64 + "\n" * 2
            articles += a.to_string() + "\n" * 2

        return feed + articles

    def __str__(self) -> str:
        """
        Overrides the standard python string convertion behavior to be able to directly call `str(document_instance)`
        and receive the correct document string representation.
        """

        return self.to_string()

    def to_dict(self) -> dict:
        articles = []
        for a in self.articles:
            articles.append(a.to_dict())
        return {"feed": self.feed, "articles": articles}

    def to_json(self, indent: Optional[int] = 2, sort_keys: Optional[bool] = False) -> str:
        """
        Returns JSON representation of a document.
        """

        self.logger.info("Converting document to JSON")
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)
