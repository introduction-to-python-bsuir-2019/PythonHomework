from src.components.logger import Logger
from abc import ABC, abstractmethod
from pathlib import Path
import conf
import urllib.request as request
from src.components.feed import FeedEntry


class ConverterAbstract(ABC):

    def __init__(self, path: str) -> None:
        self._path_initialize(Path(path))


    @abstractmethod
    def render(self, feeds_entries: list, title: str) -> str:
        pass

    @abstractmethod
    def _entry_render(self, entry: FeedEntry):
        pass

    def _path_initialize(self, path: Path):

        self._path = path

        if not self._path.parent.exists():
            self._path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

        self._media_path = Path.home()\
            .joinpath('.' + conf.__package__)\
            .joinpath('media')

        if not self._media_path.exists():
            self._media_path.mkdir(
                parents=True, exist_ok=True
            )

    def _download_media(self, media_url: str) -> bool:

        media_file = self._media_path.joinpath(
            hash(media_url)
        )

        try:
            data = request.urlretrieve(media_url)
        except(request.HTTPError, request.URLError):
            Logger.log(f'Image with url {media_url} did not download')
            return False

        with open(media_file, 'wb') as file:
            file.write(data.content)

        return media_file

    def _save_render_file(self, output, encoding: str='UTF-8') -> None:
        with open(self._path, 'w', encoding=encoding) as file:
            file.write(output)
