from django.urls import path

from .views import *

urlpatterns = [
    path('', SettingsUpdate.as_view(), name='settings_url'),
    path('news/', news_page, name='news_url'),
    path('download/json', download_json, name='dl_json_url'),
]
