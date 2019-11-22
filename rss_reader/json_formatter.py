import json
from .news import News

class FeedEncoder(json.JSONEncoder):
    def default(self, obj: object):
        if isinstance(obj, Json):  
            return {'News':[{'Feed'+str(number):{k:v for k,v in (feed.__dict__).items()} for number, feed in zip(range(len(obj.news_to_convert)),obj.news_to_convert)}]}
        return json.JSONEncoder.default(self, obj)
    

class Json(object):
    
    def __init__(self, news):
        self.news_to_convert = news
        
    def __str__(self):
        return json.dumps(self, cls=FeedEncoder, indent=4, ensure_ascii=False)
