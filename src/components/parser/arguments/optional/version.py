from .. import ArgumentsAbstract
import conf


class Version(ArgumentsAbstract):

    def add_argument(self):
        self._parser.add_argument(
            '-v', '--version', action='version', version=conf.__version__, help='Print version info'
        )
