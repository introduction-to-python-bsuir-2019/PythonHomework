from django.db import models


class NewsInfo(models.Model):
    date_id = models.IntegerField()
    pubDate = models.DateTimeField(max_length=255)
    title = models.CharField(max_length=255, unique=True)
    title_hash = models.CharField(max_length=255, default=hash('title'))
    rss_title = models.CharField(max_length=255, default='vadbeg_news')
    rss_image = models.CharField(max_length=255, default='image')
    rss_hash = models.CharField(max_length=255, default=hash('vadbeg_news'))
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    imageLink = models.CharField(max_length=255)
    imageDescription = models.CharField(max_length=255)

    def __str__(self):
        return self.title_hash

