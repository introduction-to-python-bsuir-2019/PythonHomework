from bs4 import BeautifulSoup
import json
from logging import Logger
from typing import Dict, List, Optional

from .logger import default_logger


class Content:
    """
    Represents the RSS standard article content.
    """

    @classmethod
    def from_html_tree(cls, tree: BeautifulSoup, logger: Optional[Logger] = default_logger):
        """
        Constructs new Content instance from a description HTML tree.

        Params:
            - tree (BeautifulSoup): HTML tree to parse the content from
            - logger (Logger): Logger instance to use for logging inside the method (optional)

        Returns:
            - Content class instance which contains the parsed data
        """

        # Grab the description text
        description = tree.text
        # Grab the content image `alt` attribute
        image = tree.find("img", alt=True)["alt"]

        return cls(description, image, logger)

    def __init__(self, description: str, image: str, logger: Logger):
        """
        Constructs new Content from parsed data.

        It is not recommended to call this method direclty with parsed HTML, instead use
        `Content.from_html_tree` class method.

        Params:
            - description (str): The content description text
            - image (str): Value of the `alt` attribute of the content image
            - logger (Logger): Logger instance to use for logging inside the class

        Returns:
            - The constructed Content object
        """

        self.description = description
        self.image = image
        self.logger = logger

    def to_string(self) -> str:
        """
        Returns string representation of a content.
        """

        self.logger.info("Converting article content to string")
        return f"[image: {self.image}] {self.description}"

    def __str__(self) -> str:
        """
        Overrides the standard python string convertion behavior to be able to directly call `str(content_instance)`
        and receive the correct content string representation.
        """

        return self.to_string()

    def to_dict(self) -> Dict[str, str]:
        """
        Returns the dict representation of an article content.
        """

        data = {"description": self.description, "image": self.image}
        return data

    def to_json(self, indent: Optional[int] = 2, sort_keys: Optional[bool] = False) -> str:
        """
        Returns JSON representation of an article content.
        """

        self.logger.info("Converting article content to JSON")
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)
