from components.parser.arguments.arguments_abstract import ArgumentsAbstract


class Json(ArgumentsAbstract):

    def __init__(self, parser):
        super().__init__(parser)

    def add_argument(self):
        self._parser.add_argument(
            '--json', action='store_true', help='Print result as JSON in stdout'
        )
