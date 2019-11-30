from src.components.parser.arguments.arguments_abstract import ArgumentsAbstract


class Source(ArgumentsAbstract):

    def add_argument(self):
        self._parser.add_argument(
            'source', type=str, help='RSS URL'
        )


