import datetime
import json

from django.db import models, IntegrityError


class Article(models.Model):
    title = models.TextField()
    description = models.TextField()
    dec_description = models.TextField()
    link = models.TextField(unique=True)
    pubDate = models.DateTimeField()
    media = models.TextField()
    source = models.ForeignKey('Source', on_delete=models.CASCADE, related_name='articles')
    links = models.TextField()
    dec_links = models.TextField()

    class Meta:
        ordering = ['pubDate']

    @classmethod
    def from_struct(cls, struct, source):
        try:
            if struct['pubDate'] != 'None':
                date = datetime.datetime.strptime(struct['pubDate'], "%a, %d %b %Y %H:%M")
            else:
                date = datetime.datetime.now()

            return cls.objects.create(
                title=struct['title'],
                description=struct['description'],
                dec_description=struct['dec_description'],
                link=struct['link'],
                pubDate=date,
                media=json.dumps(struct['media']),
                source=source,
                links=json.dumps(struct['links']),
                dec_links=json.dumps(struct['dec_links'])
            )
        except IntegrityError:
            return None

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'dec_description': self.dec_description,
            'link': self.link,
            'pubDate': self.pubDate.strftime("%a, %d %b %Y %H:%M"),
            'media': json.loads(self.media),
            'source': self.source.url,
            'links': json.loads(self.links),
            'dec_links': json.loads(self.dec_links),
        }
