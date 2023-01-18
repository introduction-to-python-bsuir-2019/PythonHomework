"""
Docstrings may compare list's instead of sets because of sets are unsortable and
can't be equal to the docstring literals
"""
from functools import reduce
import itertools
import string

from collections import Counter

test_strings = ["hello", "world", "python", ]


def test_1_1(*strings):
    """
    characters that appear in all strings

    >>> test_1_1("hello", "world", "python")
    {'o'}
    """
    return set(strings[0]).intersection(*strings)


def test_1_2(*strings):
    """
    characters that appear in at least one string

    >>> test_1_2("hello", "world", "python")
    ['d', 'e', 'h', 'l', 'n', 'o', 'p', 'r', 't', 'w', 'y']
    """

    return sorted(set("").union(*strings))


def test_1_3(*strings):
    """
    characters that appear at least in two strings

    >>> test_1_3("hello", "world", "python")
    ['h', 'l', 'o']
    """
    combines_by_two = list(itertools.product(strings, repeat=2))
    result = set.union(*(set(pair[0]) & set(pair[1]) for pair in combines_by_two if pair[0] != pair[1]))
    return sorted(result)


def test_1_4(*strings):
    """
    characters of alphabet, that were not used in any string

    >>> test_1_4("hello", "world", "python")
    ['a', 'b', 'c', 'f', 'g', 'i', 'j', 'k', 'm', 'q', 's', 'u', 'v', 'x', 'z']
    """
    return sorted(set(string.ascii_lowercase) - set("").union(*strings))


def generate_squares(num):
    """
    takes a number as an argument and returns a dictionary, where the key is a number and
    the value is the square of that number
    >>> generate_squares(5)
    {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
    """
    return dict([(v, v**2) for v in (range(1, num + 1))])


def count_letters(s):
    """
    takes string as an argument and returns a dictionary, that contains letters of given
    string as keys and a number of their occurrence as values

    >>> count_letters('stringsample')
    {'s': 2, 't': 1, 'r': 1, 'i': 1, 'n': 1, 'g': 1, 'a': 1, 'm': 1, 'p': 1, 'l': 1, 'e': 1}
    """
    return dict(Counter(s))


def combine_dicts(*args):
    """
    Receives changeable number of dictionaries (keys - letters, values - numbers) and combines them into one dictionary.
    Dict values should be summarized in case of identical keys

    >>> combine_dicts({'a': 100, 'b': 200}, {'a': 200, 'c': 300}, {'a': 300, 'd': 100})
    {'a': 600, 'b': 200, 'c': 300, 'd': 100}

    """
    return dict(sum((Counter(dict(x)) for x in args), Counter()))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
