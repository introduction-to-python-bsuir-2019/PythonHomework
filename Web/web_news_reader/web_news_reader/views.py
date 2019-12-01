from django.shortcuts import render
from django.http import HttpResponse


def base_page(request):
    return render(request, 'base.html')
