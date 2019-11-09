import argparse
parser = argparse.ArgumentParser(description='Pure python command-line RSS reader')
parser.add_argument("source", help = 'RSS URL', type = str)
parser.add_argument("--version", action="store_true", help = 'Print version info')
parser.add_argument("--json", metavar='', help = 'Print result as JSON in stdout', type = str)
parser.add_argument("--verbose", metavar='', help = 'Outputs verbose status messages', type = str)
parser.add_argument("--limit", help = 'Limit news topics', type = int)
args = parser.parse_args()

if args.version:
    print("Version: First iteration is coming soon")
