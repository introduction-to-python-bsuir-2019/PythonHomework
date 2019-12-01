from django.db import models


class Source(models.Model):
    title = models.TextField(null=True)
    url = models.TextField(unique=True)

    class Meta:
        ordering = ['title', ]

    @classmethod
    def get_or_create(cls, url, title=None):
        try:
            return cls.objects.get(url=url)
        except cls.DoesNotExist:
            return cls.objects.create(url=url, title=title)

    def sort_by_date(self, date):
        return self.articles.filter(pubDate__gte=date)
