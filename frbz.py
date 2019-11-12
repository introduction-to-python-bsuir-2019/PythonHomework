import args_parser
import rss_parser
import format_converter


class Reader:

    @staticmethod
    def exec_console_args():
        _args = args_parser.get_args()
        parser = rss_parser.Parser(_args.source)
        limit = _args.limit
        len_each_line = _args.length
        if len_each_line < 60:
            print("The length must be greater than 60")
            return
        if limit < 1:
            print("The limit must be greater than 0")
            return
        feeds = [parser.parse_feed(limit)]
        if feeds[0] is None:
            print("Invalid url.")
            return
        converter = format_converter.Converter(feeds)
        print(converter.to_console_format(str_len=len_each_line))


if __name__ == "__main__":
    reader = Reader()
    reader.exec_console_args()
