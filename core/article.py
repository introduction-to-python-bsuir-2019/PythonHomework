from bs4 import BeautifulSoup
import json
from logging import Logger
from typing import List, Optional
from xml.etree import ElementTree

from .content import Content
from .logger import default_logger


def find_links(tree: BeautifulSoup, logger: Optional[Logger] = default_logger) -> List[str]:
    """
    Recursively finds all links inside the given HTML string.

    This method looks both for anchor tags `href` attributes and image tags `src` attributes which start with "http"
    prefix (and, accordingly, are working links).

    Params:
        - tree (BeautifulSoup): BeautifulSoup instance contains HTML template to search for links in
        - logger (Logger): Logger instance to use for logging inside the function (optional)

    Returns:
        - List of strings which contains all the found links
    """

    links = []

    logger.info("Parsing anchor tags")

    # Iterate through all anchor tags which have `href` attribute
    for el in tree.find_all("a", href=True):
        logger.info("Got anchor element: %s", el)
        # Check that the href is an external HTTP/S link (not an element ID or email link and etc.)
        if el["href"].startswith("http"):
            logger.info("Got HTTP/S link: %s", el["href"])
            links.append(el["href"])

    logger.info("Parsing image tags")

    # Iterate through all image tags which have `src` attribute
    for el in tree.find_all("img", src=True):
        logger.info("Got image element: %s", el)
        # Check that the href is an external HTTP/S link (not an element ID or email link and etc.)
        if el["src"].startswith("http"):
            logger.info("Got HTTP/S link: %s", el["src"])
            links.append(el["src"])

    return links


def remove_duplicates(items: List, logger: Optional[Logger] = default_logger) -> List:
    """
    Returns copy of the passed array without duplicates.

    The purpose of this method is because when the `list(set(items))` is used, the original list items order is being
    destroyed. This function iterates through the whole list in sequence and adds the items to new list only if they
    have not been seen earlier, so the original list order is saved.

    Params:
        - items (list): List to remove the duplicates from
        - logger (Logger): Logger instance to use for logging inside the function (optional)

    Returns:
        - New list without duplicates
    """

    result = []
    seen_elements = set()

    logger.info("Removing duplicate items")

    for element in items:
        # Only adds new element to the resulting list if it has not been added earlier
        if not element in seen_elements:
            result.append(element)
            seen_elements.add(element)
        else:
            logger.info("Excluding duplicate item: %s", element)

    return result


class Article:
    """
    Represents the RSS standard article data.
    """

    @classmethod
    def from_xml(cls, element: ElementTree.Element, logger: Optional[Logger] = default_logger):
        """
        Constructs new Article from an XML element.

        Params:
            - element (ElementTree.Element): XML element to parse the article from
            - logger (Logger): Logger instance to use for logging inside the method (optional)

        Returns:
            - Article class instance which contains the parsed data
        """

        logger.info("Parsing %s article data", str(element))

        # Grab the article title element
        title = element.find("title")
        logger.info("Got article title: %s", title)

        # Grab the article date (`pubDate` tag)
        date = element.find("pubDate")
        logger.info("Got article date: %s", date)

        # Grab the article description
        description = element.find("description")
        logger.info("Got article description: %s", description)

        # Grab the article public link
        public_link = element.find("link")
        logger.info("Got article public link: %s", public_link)

        # Parse the description text to HTML tree
        tree = BeautifulSoup(description.text, "html.parser")
        logger.info("Parsed the HTML data")

        # Parse the description to human-readable format (with images)
        content = Content.from_html_tree(tree, logger)

        # Concatenate the array containing public link with links found in the `description` element to get complete
        # article links list
        all_links = [public_link.text]
        all_links.extend(find_links(tree, logger))

        # Remove duplicate links (article description can also contain the public link)
        all_links = remove_duplicates(all_links, logger)

        return cls(title.text, date.text, public_link.text, content, all_links, logger)

    def __init__(self, title: str, date: str, public_link: str, content: Content, links: List[str], logger: Logger):
        """
        Constructs new Article from parsed data.

        It is not recommended to call this method direclty with parsed XML, instead use `Article.from_xml` class method.

        Params:
            - title (str): The article title
            - date (str): Article creation date
            - public_link (str): Article public link from which it can be accessed within the browser
            - content (Content): Parsed article content (description)
            - links (List[str]): List of all article links
            - logger (Logger): Logger instance to use for logging inside the class

        Returns:
            - The constructed Article object
        """

        self.title = title
        self.date = date
        self.public_link = public_link
        self.content = content
        self.links = links
        self.logger = logger

    def to_string(self) -> str:
        """
        Returns string representation of an article.
        """

        self.logger.info("Converting article header to string")

        title = f"Title: {self.title}\n"
        date = f"Date: {self.date}\n"
        public_link = f"Link: {self.public_link}\n"
        content = f"\n{self.content}\n"

        self.logger.info("Converting article links to string")

        links_title = "\n\nLinks:"
        links_list = ""

        for i, l in enumerate(self.links):
            links_list += f"\n[{i + 1}]: {l}"

        return title + date + public_link + content + links_title + links_list

    def __str__(self) -> str:
        """
        Overrides the standard python string convertion behavior to be able to directly call `str(article_instance)`
        and receive the correct article string representation.
        """

        return self.to_string()

    def to_dict(self) -> dict:
        """
        Returns the dict representation of an article data.
        """

        return {
            "title": self.title,
            "date": self.date,
            "public_link": self.public_link,
            "content": self.content.to_dict(),
            "links": self.links,
        }

    def to_json(self, indent: Optional[int] = 2, sort_keys: Optional[bool] = False) -> str:
        """
        Returns JSON representation of an article.
        """

        self.logger.info("Converting article to JSON")
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)
