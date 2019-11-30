import json
import logging
from .news import News

class FeedEncoder(json.JSONEncoder):
    def default(self, obj: object):
        names_of_sections = ('Feed source', 'Title', 'Date', 'Link', 'Description', 'Media_content')
        if isinstance(obj, Json):
            logging.info('Encoding news into JSON format')
            number_of_news = len(obj.news_to_convert)
            return {'News':
                        [{'Feed'+str(number):
                                {section_name:str(feed_section) for section_name, feed_section
                                                                    in zip(names_of_sections, feed())}\
                                                                        for number, feed 
                                                                            in zip(range(number_of_news),obj.news_to_convert)}]}
        return json.JSONEncoder.default(self, obj)
    

class Json(object):
    
    def __init__(self, news):
        logging.info('Initialization of JSON formatter')
        self.news_to_convert = news
        
    def __str__(self):
        logging.info('Receiving news in JSON fromat')
        return json.dumps(self, cls=FeedEncoder, indent=4, ensure_ascii=False)
