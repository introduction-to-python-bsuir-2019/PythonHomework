from src.components.parser.arguments import ArgumentsAbstract


class Verbose(ArgumentsAbstract):

    def __init__(self, parser):
        super().__init__(parser)

    def add_argument(self):
        self._parser.add_argument(
            '--verbose', default=False, action='store_true', help='Outputs verbose status messages'
        )

