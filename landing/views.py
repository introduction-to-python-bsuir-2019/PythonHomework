from django.shortcuts import render
from .forms import MainForm
from App.RSSListener import RSSListener


def home(request):
    submitbutton = request.POST.get("submit")

    rss = ''
    limit = 20

    form = MainForm(request.POST or None)
    if form.is_valid():
        rss = form.cleaned_data.get("rss")
        limit = form.cleaned_data.get("limit")
        listener = RSSListener(limit, False, None, "./templates/news.html", None)
        listener.start(rss)

    context = {'form': form, 'rss': rss, 'limit': limit, 'submitbutton': submitbutton}

    return render(request, 'landing.html', context)


def news(request):
    return render(request, 'news.html', locals())
