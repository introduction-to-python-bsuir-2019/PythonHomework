from src.components.parser.arguments import ArgumentsAbstract


class Json(ArgumentsAbstract):

    def add_argument(self):
        self._parser.add_argument(
            '--json', action='store_true', help='Print result as JSON in stdout'
        )
