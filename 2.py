#!/usr/local/opt/python/bin/python3.7
from functools import reduce
import functools
import operator


def quotes_changer(in_str):
    """ Receives a string and replaces all " symbols with ' and vise versa

    >>> quotes_changer('String with double quotes: " " " "')
    "String with double quotes: \' \' \' \'"

    >>> quotes_changer("String with single quotes: ' ' ' '")
    'String with single quotes: " " " "'
    """

    ch1 = '"'
    ch2 = "'"
    translation_map = {ord(ch1): ch2, ord(ch2): ch1}
    out_str = in_str.translate(translation_map)
    # out_str = in_str.replace(ch1, temp_char).replace(ch2, ch1).replace(temp_char, ch2)

    return out_str


def if_str_is_palindrome(in_str):
    """ Check whether a string is a palindrome or not.

    Usage of any reversing functions is prohibited

    >>> if_str_is_palindrome("Able was I ere I saw Elba")
    True
    >>> if_str_is_palindrome("A man, a plan, a canal – Panama")
    True

    >>> if_str_is_palindrome("A man, a plan, a canal – Panam")
    False
    """
    alph_str = list(filter(str.isalnum, in_str.lower()))
    return alph_str[::-1] == alph_str


def split(inp: str) -> list:
    """
    Custom split function - works only for spaces

    >>> split('Mama washed the window frame')
    ['Mama', 'washed', 'the', 'window', 'frame']
    """
    out = []
    j = 0
    for i, ch in enumerate(inp):
        if ch == ' ':
            out.append(inp[j:i])
            j = i + 1
    else:
        out.append(inp[j:])
    return list(filter(None, out))


def split_by_index(s: str, indexes: list) -> list:
    """

    >>> split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18])
    ['python', 'is', 'cool', ',', "isn't", 'it?']

    >>> split_by_index("no luck", [42])
    ['no luck']
    """
    out = []
    j = 0
    for idx in (indexes):
        out.append(s[j:idx])
        j = idx
    else:
        out.append(s[j:])
    return list(filter(None, out))


def get_digits(di: int) -> tuple:
    """
    >>> get_digits(87178291199)
    (8, 7, 1, 7, 8, 2, 9, 1, 1, 9, 9)
    """

    return tuple(int(i) for i in str(di))


def get_longest_word(s: str) -> str:
    """
    >>> get_longest_word('Python is simple and effective!')
    'effective!'
    >>> get_longest_word('Any pythonista like namespaces a lot.')
    'pythonista'
    """
    return max(s.split(' '), key=len)


def foo(integers: list):
    """
    >>> foo([1, 2, 3, 4, 5])
    [120, 60, 40, 30, 24]
    """
    result = []
    for i, num in enumerate(integers):
        t = integers[:]
        t.pop(i)
        result.append(functools.reduce(operator.mul, t, 1))
    return result


def get_pairs(inp):
    """
    >>> get_pairs([1, 2, 3, 8, 9])
    [(1, 2), (2, 3), (3, 8), (8, 9)]
    >>> get_pairs(['need', 'to', 'sleep', 'more'])
    [('need', 'to'), ('to', 'sleep'), ('sleep', 'more')]
    >>> get_pairs([1])

    """
    return list(zip(inp[0::1], inp[1::1])) or None


def get_none():
    """
    >>> get_none()

    """
    return None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
