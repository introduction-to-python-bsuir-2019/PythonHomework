import argparse


def main():
    parser = adding_arguments()
    args = parser.parse_args()
    print(args.limit)
    #get_news(args.source, args.limit)
    

def adding_arguments():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', metavar='source', type=str, help='RSS URL')
    parser.add_argument('--version', action='version', version='ver 1.1', help='Print version info')
    parser.add_argument('--limit', metavar='LIMIT', nargs=1, type=int)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--date', nargs='+', type=int)
    return parser
        
    
if __name__=="__main__":
   main()