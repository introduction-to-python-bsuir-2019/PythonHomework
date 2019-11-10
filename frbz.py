import args_parser
import rss_parser
import format_converter


class Reader:

    @staticmethod
    def exec_console_args():
        _args = args_parser.get_args()
        parser = rss_parser.Parser(_args.source)
        items = parser.parse_feed()
        converter = format_converter.Converter(items)
        print(converter.to_console_format())


if __name__ == "__main__":
    reader = Reader()
    reader.exec_console_args()
