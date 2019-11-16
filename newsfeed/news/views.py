from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from django.db.utils import IntegrityError

from .forms import GetRSSForm
from .models import NewsInfo

from news_feed.rss_reader import NewsReader

from dateutil.parser import parse

import html


def index(request):
    return HttpResponse('You are on app page')


def add_to_news_database(items, model):
    info_all = list()

    for id_num, item in items.items():
        if id_num != 'title':
            try:
                info = model(date_id=id_num,
                             pubDate=str(parse(item['pubDate']).date()),
                             title=html.unescape(item['title']),
                             link=item['link'],
                             description=item['description'],
                             imageLink=item['imageLink'],
                             imageDescription=item['imageDescription'])

                info_all.append(info)
            except IntegrityError as e:
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


class PostListView(ListView):
    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']
