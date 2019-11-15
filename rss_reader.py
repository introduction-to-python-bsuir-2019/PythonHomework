import argparse
import reader


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("source",    type=str,            help="RSS URL")
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json",    action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit",   action="store_true", help="Limit news topics if this parameter provided")
    return parser.parse_args()


def main():
    args = parse_arguments()
    print(args)


if __name__ == "__main__":
    main()
