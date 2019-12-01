from src.components.converter.converter_abstract import ConverterAbstract
from src.components.logger import Logger
from src.components.feed import FeedEntry
from src.components.converter.html import templates as template


class HtmlConverter(ConverterAbstract):

    _extensions = ['html']

    def render(self, feeds_entries: list, url: str, title: str, encoding: str = 'UTF-8') -> str:

        self._template = template

        render_feeds_entries = []

        for index, entry in zip(range(self._limit), feeds_entries):
            render_feeds_entries.append(
                self._entry_render(entry)
            )

        self._save_render_file(
            self._template.layout.render(
                feeds_entries=render_feeds_entries,
                url=url,
                title=title,
                encoding=encoding
            )
        )

    def _media_render(self, media: list):

        media_output = []

        for item in media:
            media_file = self._download_media(item.url)

            if not media_file:
                return self._template.empty_media.render()

            media_output.append(self._template.media.render(
                src=media['url'], alt=media['alt'])
            )

        return media_output

    def _entry_render(self, entry: FeedEntry):

        return self._template.entry.render(
            media=self._media_render(entry.media),
            title=entry.title,
            date=entry.published,
            text=entry.description,
            link=entry.link,
            links=entry.links
        )
