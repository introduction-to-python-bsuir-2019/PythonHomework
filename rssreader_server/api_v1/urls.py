from django.urls import path

from .views import *

"""
    API v1.0

    /news/ 
        * method GET -> return news:
            Method GET using for take parameters.
            Optional parameters:
                * url=URL          RSS URL
                * limit=LIMIT      Limit news topics if this parameter provided
                * date=DATE        Print cached articles by date
                * to_json          Print result as JSON in browser
                * to-pdf=TO_PDF    Print result as PDF in file `TO_PDF`
                * to-html=TO_HTML  Print result as HTML in file `TO_PDF`
    /help/
        * all methods -> return info about

"""
urlpatterns = [
    path('news/', LoaderNews().download_result),
    path('help/', show_help_view)
]
