import argparse

def args():
    '''if the main() function in rss_reader.py is heart of the project
    this should be the hands. Returns arguments which we parse'''
    parser = argparse.ArgumentParser(description='Pure python command-line RSS reader')
    parser.add_argument("source", help='RSS URL', nargs="?", type=str)
    parser.add_argument("--version", action="store_true", help='Print version info')
    parser.add_argument("--json", action='store_true', help='Print result as JSON in stdout')
    parser.add_argument("--verbose", action='store_true', help='Outputs verbose status messages')
    parser.add_argument("--limit", help='Limit news topics', type=int)
    parser.add_argument("--date", help='Shows cached news on introduced day', type=int)
    parser.add_argument("--to_pdf",action='store_true', help = 'Converts news into PDF format' )
    return parser.parse_args()
