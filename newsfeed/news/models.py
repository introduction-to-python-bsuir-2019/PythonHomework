from django.db import models


class NewsInfo(models.Model):
    date_id = models.IntegerField()
    pubDate = models.DateTimeField(max_length=255)
    title = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    imageLink = models.CharField(max_length=255)
    imageDescription = models.CharField(max_length=255)

    def __str__(self):
        return self.title
