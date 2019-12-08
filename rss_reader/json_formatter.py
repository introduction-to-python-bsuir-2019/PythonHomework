'''Module contains implementation of JSON converter'''
import json
import logging
from .news import News

class FeedEncoder(json.JSONEncoder):
    """Subclass of JSONEncoder to be used for transforming into JSON"""
    def default(self, obj: object):
        '''Method returns serializable object of news'''
        names_of_sections = ('Feed source', 'Title', 'Date', 'Link', 'Description', 'Media_content')
        if isinstance(obj, Json):
            logging.info('Encoding news into JSON format')
            return {'News':
                        [{'Feed'+str(number):
                                {section_name: feed_section for section_name, feed_section
                                                                    in zip(names_of_sections, feed())}\
                                                                        for number, feed 
                                                                            in enumerate(obj.news_to_convert)}]}
        return json.JSONEncoder.default(self, obj)
    

class Json(object):
    '''Class that implements getting of the news in JSON format'''
    def __init__(self, news):
        logging.info('Initialization of JSON formatter')
        self.news_to_convert = news
        
    def __str__(self):
        '''Returns news in JSON format'''
        logging.info('Receiving news in JSON fromat')
        return json.dumps(self, cls=FeedEncoder, indent=4, ensure_ascii=False)
