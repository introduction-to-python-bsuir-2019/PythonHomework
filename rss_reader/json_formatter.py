import json
from .news import News

class FeedEncoder(json.JSONEncoder):
    def default(self, obj: object):
        if isinstance(obj, News):
            return {}
        return json.JSONEncoder.default(self, obj)
    

class Json(object):
    
    def __init__(self, obj):
        self.feed_dict = {'feed':obj.feed, 'title':obj.title, 'date':obj.date, 
                          'description':obj.description, 'links':[obj.link, obj.media_content]}
        
    def mk_json(self):
        print(json.dumps(self, cls=FeedEncoder, indent=4, encure_ascii=False))
        return json.dumps(self, cls=FeedEncoder, indent=4, encure_ascii=False)
