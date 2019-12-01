from app.rssConverter.Exeptions import IncorrectLimit


class NewsPinter:
    """Class for printing news in simple and json format"""

    @staticmethod
    def get_limited_news(dict_list, limit):
        news_quantity = len(dict_list)
        if limit is None:
            limit = news_quantity
        elif limit > news_quantity:
            raise IncorrectLimit(news_quantity)
        return dict_list[:limit]

    @staticmethod
    def print_news(news_list, limit=None):
        """printing news in readable form"""
        news_list = NewsPinter.get_limited_news(news_list, limit)
        for new in news_list:
            for key, item in new.items.items():
                if key == 'links':
                    print("\n")
                    print(key)
                    for href in item:
                        print("\n")
                        print(href)
                else:
                    if item == 'Unknown' and key in ['pubDate', 'published']:
                        continue
                    print("\n")
                    print(key + '    ' + item)
            print('-----------------------------------------------------------------------------------')

    @staticmethod
    def in_json_format(news_list, limit):
        """Writing news in json format"""
        news_list = NewsPinter.get_limited_news(news_list, limit)
        json_str = '{'
        json_str += ' ' + '"news":'
        json_str += ' ' + '['
        for new in news_list:
            json_str += ' ' + '{'
            for key, item in new.items.items():
                if item is not None:
                    if key == 'links':
                        key = NewsPinter.to_str_for_json(key)
                        json_str += " " + key + ':'
                        json_str += " " + '['
                        for link in item:
                            link = NewsPinter.to_str_for_json(link)
                            json_str += " " + link + ','
                        json_str = json_str[:-1]
                        json_str += " " + '],'
                    else:
                        if item == 'Unknown' and key in ['pubDate', 'published']:
                            continue
                        key = NewsPinter.to_str_for_json(key)
                        item = NewsPinter.to_str_for_json(item)
                        json_str += " " + key + ':' + item + ','
            json_str = json_str[:-1]
            json_str += " " + '},'
        json_str = json_str[:-1]
        json_str += " " + ']'
        json_str += '}'
        return json_str

    @staticmethod
    def to_str_for_json(value):
        """Converting python string to json string"""
        value = value.replace('"', "'")
        value = value.replace('/', " ")
        value = value.replace('\\', " ")
        return '"' + str(value) + '"'
