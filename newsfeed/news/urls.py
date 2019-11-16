from django.urls import path

from .views import index, rss_source, PostListView
from .forms import GetRSSForm

urlpatterns = [
    path('', index, name='index'),
    path('rss-source/', rss_source, name='rrs_source'),
    path('home/', PostListView.as_view(), name='home')
]