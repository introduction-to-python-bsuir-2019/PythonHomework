import argparse


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("source",help="RSS URL",type=str)
    parser.add_argument("--version",action='version', version='%(prog)s '+'v 1.0',help="Print version info", )
    parser.add_argument("--json",help="Print result as JSON in stdout",action="store_true")
    parser.add_argument("--verbose",help="Outputs verbose status messages",action="store_true")
    parser.add_argument("--limit",type=int,help="Limit news topics if this parameter provided")
    args = parser.parse_args()


if  __name__=="__main__":
    args()