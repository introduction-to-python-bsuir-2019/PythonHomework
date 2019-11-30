import argparse

def get_args():
    parser = argparse.ArgumentParser(description = "Simple rss-reader")
    parser.add_argument("URL", type = str, help = "URL to rss sourse")
    parser.add_argument("-l", "--limit", type = int, help = "Set quantity of news")
    parser.add_argument("-v","--version", action = "store_true", help = "Print version info")
    parser.add_argument("--json", action = "store_true", help = "Print result as JSON")
    parser.add_argument("--colorize", action = "store_true", help = "Print the result of the utility in colorized mode")
    parser.add_argument("--verbose", action = "store_true", help = "Outputs verbose status messages")
    parser.add_argument("-d", "--date", type = str, help = "Set date in YMD format for searching in cashed news")
    parser.add_argument("--to-fb2", action = "store_true", help = "In the activated state, the program creates a News.fb2 file in the working directory")
    parser.add_argument("--to-pdf", action = "store_true", help = "In the activated state, the program creates a News.pdf file in the working directory")
    args = parser.parse_args()
    return args

args = get_args()
