import datetime

import feedparser
from django.http import HttpResponse, Http404

from api_v1.feed_parser import Parser
from api_v1.storage_controller import StorageController
from api_v1.view_controller import ResponseController


class LoaderNews:
    def download_result(self, request):
        """
        Method of process request

        :param request: request struct for processing
        :type: dict
        :return: response of process URL
        :rtype: HttpResponse
        """
        if request.method == 'GET':
            kwargs = {
                'url': request.GET.get('url', None),
                'date': request.GET.get('date', None),
                'limit': request.GET.get('limit', None),
                'to_pdf': request.GET.get('to_pdf', None),
                'to_json': request.GET.get('to_json', None),
                'to_html': request.GET.get('to_html', None),
            }
            return self._execute(**kwargs)
        else:
            return Http404()

    def _execute(self, url, limit, date, **kwargs):
        """
        Main method of processing request.

        :param url: URL RSS
        :param limit: count of output articles, if given
        :param date: datetime, need for load caching from storage
        :param kwargs: optional parameters
        :type url: str
        :type limit: str
        :type date: str
        :type kwargs: dict
        :return: http response of processing request
        :rtype: HttpResponse
        """
        if limit:
            try:
                limit = int(limit)
                if limit < 1:
                    return HttpResponse(f"Bad given value limit '{limit}'", status=404)
            except (ValueError, TypeError):
                return HttpResponse(f"Bad given value limit '{limit}'", status=404)

        if not date:
            articles = self._get_articles_from_url(url, limit)

            StorageController.save(url, articles['articles'], articles['title'])
        else:
            try:
                datetime.datetime.strptime(date, "%Y%m%d")
            except ValueError:
                return HttpResponse(f"Error format date {date}. Need '%Y%m%d'", status=404)
            articles = StorageController.load(url, datetime.datetime.strptime(date, "%Y%m%d"), limit)

        return ResponseController.load_result_into_file(articles,
                                                        to_html=kwargs.get('to_html', None),
                                                        to_json=kwargs.get('to_json', None),
                                                        to_pdf=kwargs.get('to_pdf', None),
                                                        to_sample=datetime.datetime.now().strftime("%d%m%Y%H%M%S"))

    @staticmethod
    def _get_articles_from_url(url, limit):
        """
        Method for downloading articles from given URL.

        :param url: RSS URL
        :param limit: count of output articles, if given
        :type url: str
        :type limit: int
        :return: dict with parsed articles
        :rtype: dict
        """
        if 'status' not in (response := feedparser.parse(url.strip())) or len(response['entries']) == 0:
            return HttpResponse(f"Error: Impossible parse RSS Feeds from url '{url}'", status=404)

        if response['status'] in range(200, 300):
            pass
        else:
            return HttpResponse(f"Error connecting with URL '{url.strip()}' with status code {response['status']}.",
                                status=404)

        return Parser.parse(response, limit)


def show_help_view(request):
    """
    Method for output info about.

    :return: http response with info about API of current app
    :rtype: HttpResponse
    """
    html_result = f"<!DOCTYPE html>" \
                  f"<html>" \
                  f"<head>" \
                  f"<meta charset='utf-8'>" \
                  f"<title>RSS Feeds</title>" \
                  f"</head>" \
                  f"<body>" \
                  f"<plaintext>Method GET using for take parameters." \
                  f"Optional parameters:" \
                  f"\n\t* url=URL          RSS URL" \
                  f"\n\t* limit=LIMIT      Limit news topics if this parameter provided" \
                  f"\n\t* date=DATE        Print cached articles by date" \
                  f"\n\t* to_json          Print result as JSON in browser" \
                  f"\n\t* to-pdf=TO_PDF    Print result as PDF in file `TO_PDF`" \
                  f"\n\t* to-html=TO_HTML  Print result as HTML in file `TO_PDF`</plaintext>" \
                  f"</body>" \
                  f"</html>"
    return HttpResponse(html_result)
