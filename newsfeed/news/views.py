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


def add_to_database(info, model):
    pass


def rss_source(request):
    if request.method == 'POST':
        form = GetRSSForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['rss_source']

            news_reader = NewsReader(url)
            items = news_reader.items

            for id_num, item in items.items():
                if id_num != 'title':
                    try:
                        info = NewsInfo(date_id=id_num,
                                        pubDate=str(parse(item['pubDate']).date()),
                                        title=html.unescape(item['title']),
                                        link=item['link'],
                                        description=item['description'],
                                        imageLink=item['imageLink'],
                                        imageDescription=item['imageDescription'])

                        info.save()
                    except IntegrityError as e:
                        pass

            return redirect('home')

    else:
        form = GetRSSForm()

    return render(request, 'news/rss_source.html', {'form': form})


class PostListView(ListView):
    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']
