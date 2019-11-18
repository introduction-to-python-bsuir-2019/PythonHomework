from io import BytesIO
import os

from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings

import xhtml2pdf.pisa as pisa


class Render:

    @staticmethod
    def fetch_resources(uri, rel):
        """
        Retrieves embeddable resource from given ``uri``.
        For now only local resources (images, fonts) are supported.
        :param str uri: path or url to image or font resource
        :returns: path to local resource file.
        :rtype: str
        :raises: :exc:`~easy_pdf.exceptions.UnsupportedMediaPathException`
        """
        if settings.STATIC_URL and not uri.startswith('http'):
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
            path = path.replace("\\", "/")
        else:
            path = uri

        # if not os.path.isfile(path):
        #     raise UnsupportedMediaPathException(
        #         "media urls must start with {} or {}".format(
        #             settings.MEDIA_ROOT, settings.STATIC_ROOT
        #         )
        #     )

        return path

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)

        html = template.render(params)
        response = BytesIO()
        pdf = pisa.CreatePDF(BytesIO(html.encode('UTF-8')),
                             response, encoding='UTF-8',
                             link_callback=Render.fetch_resources)

        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse('Error Rendering PDF', status=400)



