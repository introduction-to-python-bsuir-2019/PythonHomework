from src.components.parser.arguments import ArgumentsAbstract


class Limit(ArgumentsAbstract):

    def __init__(self, parser):

        super().__init__(parser)

    def add_argument(self):
        self._parser.add_argument(
            '--limit', type=int, default=3, help='Limit news topics if this parameter provided'
        )

