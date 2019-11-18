import json
from .news import News

class FeedEncoder(json.JSONEncoder):
    def default(self, obj: object) -> Dict:
        if isinstance(obj, News):
            return {}
        return json.JSONEncoder.default(self, obj)
    

class Json(object):
    
    def __init__(self, feed, title, date, description, links):
        self.feed_dict = {'feed':feed, 'title':title, 'date':date, 'description':description, 'links':links}
        
    def mk_json(self):
        json.dumps(self, cls=FeedEncoder, indent=4, encure_ascii=False).
