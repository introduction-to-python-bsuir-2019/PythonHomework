from django.shortcuts import render, redirect
from django.views.generic import ListView, View

from django.db.utils import IntegrityError
from django.db.models import Q

from django.http import HttpResponse

from .forms import GetRSSForm
from .models import (NewsInfo)
from .render import Render as PdfRender

from news_feed.rss_reader import NewsReader
from news_feed.format_converter import FB2NewsConverter

import html


def index(request):
    """
    View for redirecting into home page

    :param request:
    :return:
    """

    return redirect('home')


def add_to_news_database(items, model):
    """
    Adds news from dict() into model

    :param items: news in dict()
    :param model: model in which we push our dict
    :return:
    """

    info_all = list()
    rss_title = "no title"
    rss_image = 'no image'

    for id_num, item in items.items():
        if id_num == 'title':
            rss_title = item

        elif id_num == 'title_image':
            rss_image = item
            print(rss_image)
        else:
            try:
                date = NewsReader.get_date(item['pubDate'])
                date_id = ''.join(str(date).split('-'))

                info = model(date_id=date_id,
                             pubDate=str(date),
                             title=html.unescape(item['title']),
                             title_hash=hash(item['title']),
                             rss_title=rss_title,
                             rss_image=rss_image,
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
    """
    View for adding new rss source

    :param request:
    :return: redirects to home
    """

    if request.method == 'POST':
        form = GetRSSForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['rss_source']

            news_reader = NewsReader(url)
            news_reader.add_news()
            items = news_reader.items

            add_to_news_database(items, NewsInfo)

            return redirect('home')

    else:
        form = GetRSSForm()

    return render(request, 'news/rss_source.html', {'form': form})


def remove_data(model):
    """
    Removes all data from model

    :param model: model with news
    :return: None
    """

    model.objects.all().delete()
    print('Have been removed!')


def remove_news(request):
    """
    View for removing all news from page

    :param request:
    :return: redirects to home page
    """

    if request.method == 'GET':
        remove_data(NewsInfo)

    return redirect('home')


class PostListView(ListView):
    """
        View for main home page with all news.
    """

    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class DatePostListView(ListView):
    """
        View for main home page with news by date.
    """

    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        print('DatePostListView query')
        query = self.model.objects.filter(date_id=self.kwargs.get('date_id'))

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class RSSPostListView(ListView):
    """
        View for main home page with news by rss.
    """

    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.model.objects.filter(rss_hash=self.kwargs.get('rss_hash'))  #!@!@!@

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class SearchResultView(ListView):
    """
        View for main home page with news by search query.
    """

    model = NewsInfo
    template_name = 'news/home.html'
    context_object_name = 'posts'
    ordering = ['-pubDate']
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query')

        print(query)
        query = self.model.objects.filter(
            Q(description__icontains=query) |
            Q(pubDate__icontains=query) |
            Q(date_id__icontains=query) |
            Q(title__icontains=query)
        )

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


def get_news_titles(post_names):
    """
    Function for getting news names
    from query name (string)

    :param post_names: query name (string)
    :return: news names
    """

    names = post_names.split('NewsInfo: ')[1:]
    names = list(map(lambda x: x[:x.find('>')], names))

    return names


class PdfView(View):
    """
        View for rendering pdf
    """

    def get(self, request, posts):
        post_names = get_news_titles(posts)

        posts = NewsInfo.objects.filter(title_hash__in=post_names)

        params = {
            'posts': posts,
            'request': request
        }

        return PdfRender.render('pdf/pdf.html', params)


def download_fb2(request, posts):
    """
    Function for handling "Export to FB2" button

    :param request:
    :param posts: query name (string)
    :return: file with fb2
    """

    post_names = get_news_titles(posts)
    posts = NewsInfo.objects.filter(title__in=post_names)

    items = dict()

    items.setdefault('title', '')

    for news in posts.values():
        items['title'] = news['rss_title']

        items.setdefault(news['id'], dict())

        items[news['id']]['title'] = news['title']
        items[news['id']]['link'] = news['link']
        items[news['id']]['pubDate'] = news['pubDate']
        items[news['id']]['description'] = news['description']
        items[news['id']]['imageLink'] = news['imageLink']
        items[news['id']]['imageDescription'] = news['imageDescription']

    fb2 = FB2NewsConverter(items)
    fb2.output('news.fb2')

    filename = 'news.fb2'

    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type=f'file/fb2')
        response['Content-Disposition'] = 'attachment; filename="news.fb2"'

        return response
