from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View

from django.db.utils import IntegrityError
from django.db.models import Q
from django.db.models import Model

from .forms import GetRSSForm
from .models import (NewsInfo,
                     LastNewsInfo)
from .render import Render as PdfRender

from news_feed.rss_reader import NewsReader

import html
from inspect import isclass


def index(request):
    return redirect('home')


def add_to_news_database(items, model):
    info_all = list()
    rss_title = "no title"

    for id_num, item in items.items():
        if id_num == 'title':
            rss_title = item
        else:
            try:
                date = NewsReader.get_date(item['pubDate'])
                date_id = ''.join(str(date).split('-'))

                info = model(date_id=date_id,
                             pubDate=str(date),
                             title=html.unescape(item['title']),
                             rss_title=rss_title,
                             rss_hash=hash(rss_title),
                             link=item['link'],
                             description=item['description'],
                             imageLink=item['imageLink'],
                             imageDescription=item['imageDescription'])

                info_all.append(info)
            except IntegrityError as e:  # it cannot be caused
                pass

    # We should ignore conflicts because of UNIQUE values. We cannot add them into database
    model.objects.bulk_create(info_all, ignore_conflicts=True)
    # This way of adding row into database is highly efficient


def rss_source(request):
    if request.method == 'POST':
        form = GetRSSForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['rss_source']

            news_reader = NewsReader(url)
            items = news_reader.items

            add_to_news_database(items, NewsInfo)

            return redirect('home')

    else:
        form = GetRSSForm()

    return render(request, 'news/rss_source.html', {'form': form})


def remove_data(model):
    model.objects.all().delete()
    print('Have been removed!')


def add_data(model, data):
    news_all = list()
    for el in data.values():
        news_entry = LastNewsInfo(date_id=el['date_id'],
                                  pubDate=el['pubDate'],
                                  title=el['title'],
                                  rss_title=el['rss_title'],
                                  rss_hash=el['rss_hash'],
                                  link=el['link'],
                                  description=el['description'],
                                  imageLink=el['imageLink'],
                                  imageDescription=el['imageDescription'])
        news_all.append(news_entry)

    model.objects.bulk_create(news_all, ignore_conflicts=True)


def remove_news(request):
    if request.method == 'GET':
        remove_data(NewsInfo)

    return redirect('home')


base = None


class PostListView(ListView):
    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']
    paginate_by = 10

    def __init__(self):
        super(PostListView, self).__init__()

        global base
        base = NewsInfo

    # def get_queryset(self):
    #     base = self.model.objects.all()

        # remove_data(LastNewsInfo)
        # add_data(LastNewsInfo, base)

        # return base


# class RemovePostListView(ListView):
#     remove_data(NewsInfo)
#     model = NewsInfo
#
#     template_name = 'news/home.html'
#     context_object_name = 'posts'
#     ordering = ['-pubDate']


class DatePostListView(ListView):
    model = NewsInfo
    template_name = 'news/news_by_date.html'
    context_object_name = 'posts'

    print('DatePostListView')

    def get_queryset(self):
        print('DatePostListView query')
        # post = get_object_or_404(Ne)/
        global base
        base = self.model.objects.filter(date_id=self.kwargs.get('date_id'))

        # remove_data(LastNewsInfo)
        # add_data(LastNewsInfo, base)

        return base


class RSSPostListView(ListView):
    model = NewsInfo
    template_name = 'news/news_by_rss.html'
    context_object_name = 'posts'
    print('RSSPostListView')

    def get_queryset(self):
        print('WTF, i\'l try to')
        global base
        base = self.model.objects.filter(rss_hash=self.kwargs.get('rss_hash'))  #!@!@!@

        # remove_data(LastNewsInfo)
        # add_data(LastNewsInfo, base)

        return base


class SearchResultView(ListView):
    model = NewsInfo
    template_name = 'news/news_by_date.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']

    def get_queryset(self):
        query = self.request.GET.get('query')
        print('WTF')
        print(query)

        global base
        base = self.model.objects.filter(
            Q(description__icontains=query) |
            Q(pubDate__icontains=query) |
            Q(date_id__icontains=query) |
            Q(title__icontains=query)
        )

        # remove_data(LastNewsInfo)
        # add_data(LastNewsInfo, base)

        return base


class PdfView(View):

    def get(self, request):
        global base
        posts = base

        if isclass(posts) and issubclass(posts, Model):
            posts = posts.objects.all()

        params = {
            'posts': posts,
            'reqeust': request
        }

        return PdfRender.render('pdf/pdf.html', params)
