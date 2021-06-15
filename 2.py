#!/usr/local/opt/python/bin/python3.7
from functools import reduce
import functools
import operator
import os



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
        t = integers[:]  # making a copy
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


def get_sums(inp: list):
    """
    >>> get_sums([1, 2, 3, 4])
    [1, 3, 6, 10]
    """
    # result = []
    # for idx, d in enumerate(inp):
    #     result.append(sum(inp[0:idx + 1]))
    return [sum(inp[0:idx + 1]) for idx in range(len(inp))]


def get_target_array(inp: list, target_value: int):
    """
    >>> get_target_array([1, 3, 7, 10], 11)
    [0, 3]
    """
    
    for i in inp:
        if i < target_value:
            pair = target_value - i
            if pair in inp:
                # print(f"the first number= {i} the second number {pair}")
                return[inp.index(i), inp.index(pair)]
            break


def get_target_array_dict(list_, target_value):
    hash_table = {}
    len_list = len(list_)
    result = []
    for item in range(len_list):
        if list_[item] in hash_table:
            result.extend([hash_table[list_[item]], item])
        else:
            hash_table[target_value - list_[item]] = item
    return result


def F(n: int):
    '''returns value of the n-th element of Fibonacci sequence'''
    if n == 0: return 0
    elif n == 1: return 1
    else: return F(n-1)+F(n-2)


def fibonacci(n: int):
    ''' Returns the Fibonacci sequence of the length '''
    r = []
    for i in range(10):
        r.append(F(i))
    print(r)


def get_none():
    """
    >>> get_none()

    """
    return None


if __name__ == "__main__":
    debug = os.environ.get('DEBUG')
    if not debug:
        import doctest

        doctest.testmod()
    else:
        # split('Mama washed the window frame')
        # get_sums([1, 2, 3, 4])
        # fibonacci(10)
        get_target_array([1, 3, 7, 10], 11)
