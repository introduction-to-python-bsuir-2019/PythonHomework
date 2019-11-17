from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, View

from django.db.utils import IntegrityError
from django.db.models import Q

from django.core.paginator import Paginator

from .forms import GetRSSForm
from .models import NewsInfo
from .render import Render as PdfRender

from news_feed.rss_reader import NewsReader

from dateutil.parser import parse

import html


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


def remove_news(request):
    if request.method == 'GET':
        remove_data(NewsInfo)

    return redirect('home')


class PostListView(ListView):
    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']
    paginate_by = 10


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
        return NewsInfo.objects.filter(date_id=self.kwargs.get('date_id'))


class RSSPostListView(ListView):
    model = NewsInfo
    template_name = 'news/news_by_rss.html'
    context_object_name = 'posts'
    print('RSSPostListView')

    def get_queryset(self):
        print('WTF, i\'l try to')
        return NewsInfo.objects.filter(rss_hash=self.kwargs.get('rss_hash'))  #!@!@!@


class SearchResultView(ListView):
    model = NewsInfo
    template_name = 'news/news_by_date.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']

    def get_queryset(self):
        query = self.request.GET.get('query')
        print('WTF')
        print(query)

        return NewsInfo.objects.filter(
            Q(description__icontains=query) |
            Q(pubDate__icontains=query) |
            Q(date_id__icontains=query) |
            Q(title__icontains=query)
        )


class PdfView(View):

    def get(self, reqeust):
        posts = NewsInfo.objects.all()
        # today = ti

        params = {
            'posts': posts,
            'reqeust': reqeust
        }

        return PdfRender.render('pdf/pdf.html', params)
