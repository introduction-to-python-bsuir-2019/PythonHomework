from src.components.parser.arguments import ArgumentsAbstract


class Colorize(ArgumentsAbstract):

    def __init__(self, parser):
        super().__init__(parser)

    def add_argument(self):
        self._parser.add_argument(
            '--colorize', default=False, action='store_true', help='Colorize console output'
        )
