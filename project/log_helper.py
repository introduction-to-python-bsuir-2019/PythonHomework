def stdout_write(string, sep=' ', end='\n', flush=False, verbose=True, color="", colorize=False):
    """Output function for singe string but convert &#39; to '"""
    if colorize:
        RED = '\033[31m'
        BLUE = '\033[34m'
        GREEN = '\033[92m'
        RESET = '\033[0m'
        
        if color == "red":
            color = RED
        elif color == "blue":
            color = BLUE
        elif color == "green":
            color = GREEN
        else:
            color, RESET = "", ""
    else:
        RED, BLUE, GREEN, RESET = "", "", "", ""

    if verbose:
        string = string.replace("&#39;", "'")
        print(color+string+RESET, sep=sep, end=end, flush=flush)


def write_progressbar(elems, done, length=20):
    """Take arguments
    elems: count of elements
    done: progress (in elements)
    length: progress bar length
    Write progress bar to stdout
    """
    if done != 0:
        print("\r", end="")
    col = int(length * (done/elems))
    print(f"[{'='*col + ' '*(length-col)}] {int(100*done/elems)}%", end="")
    if elems == done:
        print()
