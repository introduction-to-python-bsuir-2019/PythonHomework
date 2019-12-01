from src.components.logger import Logger
from abc import ABC, abstractmethod
from pathlib import Path
import conf
import urllib.request as request
from src.components.feed import Feed
from src.components.feed import FeedEntry
import jinja2


class ConverterAbstract(ABC):

    _media_img_ext = '.jpg'

    def __init__(self, path: str, limit: int) -> None:
        self._path_initialize(Path(path))
        self._limit = limit

    @abstractmethod
    def render(self, feed: Feed) -> str:
        pass

    @abstractmethod
    def _entry_render(self, entry: FeedEntry):
        pass

    @abstractmethod
    def _media_render(self, entry: FeedEntry):
        pass

    def _init_template_processor(self, template_path: str):
        path = str(Path(__file__).parent.joinpath(template_path).as_posix())

        self._template_processor = jinja2.Environment(
            loader=jinja2.FileSystemLoader(path), trim_blocks=True
        )

    def _path_initialize(self, path: Path):

        self._path = path

        if not self._path.parent.exists():
            self._path.parent.mkdir(
                parents=True,
                exist_ok=True
            )
        else:
            Logger.log(f'Caution - file {self._path} would be overriding')

        self._media_path = Path.home()\
            .joinpath('.' + conf.__package__)\
            .joinpath('media')

        if not self._media_path.exists():
            self._media_path.mkdir(
                parents=True, exist_ok=True
            )

    def _download_media(self, media_url: str) -> bool:

        media_file_name = str(abs(hash(media_url)) % 10 ** 10)

        media_file = self._media_path.joinpath(media_file_name + self._media_img_ext)

        try:
            request.urlretrieve(media_url, media_file)
            media_file.chmod(0o755)

        except(request.HTTPError, request.URLError):
            Logger.log(f'Image with url {media_url} did not download')
            return False

        return media_file

    def _save_render_file(self, output, encoding: str='UTF-8') -> None:

        with open(self._path, 'w', encoding=encoding) as file:
            file.write(output)

        Path(self._path).chmod(0o755)

