from components.parser import parser


def main():
    parser.Parser(
        'Pure Python command-line RSS reader.',
        'rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source'
    )


if __name__ == "__main__":
    main()
