def main():
    parser = adding_arguments()

    args = parser.parse_args()
    get_news(args.source, args.limit)
    
    
if __name__=="__main__":
   main()