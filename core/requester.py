from logging import Logger
from requests import get
from sys import exit
from typing import Optional
from xml.etree import ElementTree

from .logger import default_logger


def request_xml(url: str, logger: Optional[Logger] = default_logger) -> ElementTree.Element:
    """
    Uses HTTP GET method to request the content of the and returns the XML parser from it.

    Params:
        - url (str): The URL to query XML from

    Returns:
        - ElementTree.Element instance which can be used to interact with the queried XML
    """

    logger.info("Sending GET request to %s", url)
    response = get(url)
    logger.info("%s responded with %s", url, str(response))

    # Validate that the server responded without errors (or with "200" status code)
    if response.status_code != 200:
        msg = f"Request to {url} failed with code: {response.status_code}"
        logger.error(msg)
        raise Exception(msg)

    # Additionaly, check that the response is "ok" (for some unexpected cases)
    if not response.ok:
        msg = f"Failed to send the request to {url}"
        logger.error(msg)
        raise Exception(msg)

    logger.info("Parsing XML from response text")

    try:
        xml = ElementTree.fromstring(response.text)
        logger.info("Parsed XML: %s", str(xml))
        return xml
    except Exception as e:
        msg = f"Failed to parse the XML: {e}"
        logger.error(msg)
        raise Exception(msg)
