from .arguments_abstract import ArgumentsAbstract


class Version(ArgumentsAbstract):

    def __init__(self, parser):
        super().__init__(parser)

    def add_argument(self):
        self._parser.add_argument(
            '-v', '--version', help='Show script version'
        )
