import requests
import xml.etree.ElementTree as ET


def get_news(url, limit=None):
    request = requests.get('https://news.yahoo.com/rss')

    result = request.text
    tree = ET.fromstring(result)

    items = dict()
    items.setdefault('title', ' ')

    for head_el in tree[0]:
        if head_el.tag == 'title':
            items['title'] = head_el.text

    for num, item in enumerate(tree.iter('item')):

        if limit is not None and limit == num:
            break

        items.setdefault(num, {})

        news_description = dict()

        for description in item:
            news_description[description.tag] = description.text

        items[num].update(news_description)

    return items


def get_image(description):
    pass


def fancy_output():
    pass


print(get_news('https://news.yahoo.com/rss'))
