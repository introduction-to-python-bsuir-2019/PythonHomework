import args_parser
import rss_parser
import format_converter


class Reader:

    @staticmethod
    def exec_console_args():
        _args = args_parser.get_args()
        parser = rss_parser.Parser(_args.source)
        limit = _args.limit
        to_json = _args.json

        if limit < 1 and limit != -1:
            print("The limit must be -1 or greater than 0")
            return
        feeds = [parser.parse_feed(limit)]
        if feeds[0] is None:
            print("Invalid url.")
            return

        len_each_line = _args.length
        if len_each_line < 60:
            print("The length must be greater than 60")
            return
        converter = format_converter.Converter(feeds)
        if to_json:
            print(converter.to_json_format(str_len=len_each_line))
        else:
            print(converter.to_console_format(str_len=len_each_line))


if __name__ == "__main__":
    reader = Reader()
    reader.exec_console_args()
