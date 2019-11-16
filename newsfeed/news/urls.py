from django.urls import path

from .views import (index,
                    rss_source,
                    PostListView,
                    DatePostListView,
                    RSSPostListView,
                    SearchResultView)


urlpatterns = [
    # path('', index, name='index'),
    path('', rss_source, name='rrs_source'),
    path('home/', PostListView.as_view(), name='home'),
    path('home/date/<str:date_id>',
         DatePostListView.as_view(),
         name='news-by-date'),
    path('home/rss_source/<str:rss_hash>',
         RSSPostListView.as_view(),
         name='news-by-rss'),
    path('home/search/',
         SearchResultView.as_view(),
         name='search-result')
]
