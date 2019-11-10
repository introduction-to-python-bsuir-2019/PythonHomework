import textwrap
import functools


class Converter:
    def __init__(self, items):
        self.__items = items

    def to_console_format(self):
        str_len = 80
        strings = []
        for item in self.__items:
            strings.append("-" * str_len)
            strings.append(f"Feed: {item.get('feed_title')}")
            strings.append(f"Author: {item.get('item_author')}")
            strings.append(f"Date: {item.get('item_date')}")
            strings.append("\n")
            strings.append(f"Title: {item.get('item_title')}")
            strings.append(f"Description: {item.get('item_description')}")
            strings.append("-" * str_len)
            strings.append("\n")
        strings = map(lambda s: textwrap.fill(s, width=str_len) + "\n", strings)

        result_string = "-" * str_len + "\n"
        result_string += functools.reduce(lambda a, b: a + b, strings)

        return result_string
