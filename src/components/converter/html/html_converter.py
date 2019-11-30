from src.components.converter.converter_abstract import ConverterAbstract
from src.components.logger import Logger
from src.components.feed import FeedEntry
from .templates import *


class HtmlConverter(ConverterAbstract):

    def render(self, feeds_entries: list, title: str, encoding: str='UTF-8') -> str:

        render_feeds_entries = []
        for entry in feeds_entries:

            render_feeds_entries.append(
                entry_templ.render(
                    # images=images_html,
                    title=entry.title,
                    date=entry.date,
                    text=entry.description,
                    link=entry.link,
                    links=entry.links
                )
            )

        self._save_render_file(
            layout_templ.render(
                feeds_entries=render_feeds_entries,
                title=title,
                encoding=encoding
            )
        )

    def _media_render(self, entry: FeedEntry):
        #make loop!!
        media = self._download_media(entry)

        if not media:
            return empty_media_templ.render()

        return media_templ.render(src=media, alt=entry.title)

    def _entry_render(self, entry: FeedEntry):
        media = self._download_media(entry)

        if not media:
            return empty_media_templ.render()

        return media_templ.render(src=media, alt=entry.title)
