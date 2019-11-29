from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.views.generic import View
from django.contrib import messages

import sys
import os

from .app_logic.rss_parser import RssReader
from .forms import SettingsForm, FORMATS_DICT

# LINK = 'https://news.yahoo.com/rss/'
LINK = 'https://news.tut.by/rss/index.rss'


class SettingsUpdate(View):
    def get(self, request):
        form = SettingsForm()
        return render(request, 'rss_reader/settings.html', context={'form': form})

    def post(self, request):
        form = SettingsForm(request.POST)
        if form.is_valid():

            rss = RssReader(request.POST['link'])

            format_ = FORMATS_DICT.get(int(request.POST['format_']))

            limit = int(request.POST['limit'])

            if format_ == 'Read on website':
                news_list = rss._get_news_as_list(limit=limit)
                return render_to_response('rss_reader/news.html', context={'news': news_list})
            elif format_ == 'Save as json':

                file_name = 'news.json'
                rss.get_news_as_json(limit=limit, filepath=file_name)

            elif format_ == 'Save as .fb2':

                file_name = 'news.fb2'
                rss.get_news_as_fb2(limit=limit, filepath=file_name)

            elif format_ == 'Save as .pdf':

                file_name = 'news.pdf'
                rss.get_news_as_pdf(limit=limit, filepath=file_name)

            with open(file_name, 'rb') as file:
                response = HttpResponse(file)
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response

        return render(request, 'rss_reader/settings.html', context={'form': form})


def news_page(request):
    rss = RssReader(link)
    news_list = rss._get_news_as_list(limit=limit)

    return render(request, 'rss_reader/news.html', context={'news': news_list})
