from components.parser.arguments.arguments_abstract import ArgumentsAbstract


class Version(ArgumentsAbstract):

    def __init__(self, parser):
        super().__init__(parser)

    def add_argument(self):
        self._parser.add_argument(
            '-v', '--version', action='version', version='%(prog)s 1.0', help='Print version info'
        )
