from components.parser.arguments.arguments_abstract import ArgumentsAbstract


class Source(ArgumentsAbstract):

    def __init__(self, parser):
        super().__init__(parser)

    def add_argument(self):
        self._parser.add_argument(
            'source', type=str, help='RSS URL'
        )


