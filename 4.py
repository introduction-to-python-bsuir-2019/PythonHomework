import csv
import os
import string

from collections import Counter, namedtuple
from functools import wraps


# 4.1
def sort_unsorted_names():
    """Sorts usorted names in the data/unsorted_names.txt file
    and stores sorted names into the data/sorted_names.txt
    """
    with open(os.path.join('data', 'unsorted_names.txt'), 'r') as f:
        names = f.read()

    with open(os.path.join('data', 'sorted_names.txt'), 'w') as f:
        f.write('\n'.join(sorted(names.split())))


# 4.2
def most_common_words(filepath='lorem_ipsum.txt', number_of_words=3):
    """search for most common words in the file

    >>> most_common_words('lorem_ipsum.txt')
    ['donec', 'etiam', 'aliquam']

    >>> most_common_words('lorem_ipsum.txt', 5)
    ['donec', 'etiam', 'aliquam', 'aenean', 'maecenas']
    """
    with open(os.path.join('data', filepath), 'r') as f:
        words = f.read()

    # remove punctuation
    words = words.translate(words.maketrans('', '', string.punctuation))

    # lowercase:
    words = words.lower()

    return [item[0] for item in Counter(words.split()).most_common(number_of_words)]


# 4.3.1
Student = namedtuple("Student", ["name", "age", "average_mark"])


def get_top_performers(file_path, number_of_top_students=5):
    """
    returns names of top performer students

    >>> get_top_performers("students.csv")
    ['Josephina Medina', 'Teresa Jones', 'Richard Snider', 'Jessica Dubose', 'Heather Garcia']

    """
    with open(os.path.join('data', file_path), 'r') as infile:
        next(infile)  # skip header line
        reader = csv.reader(infile)

        students = [Student(row[0], row[1], row[2]) for row in reader]
    sorted_students_by_marks = sorted(students, key=lambda x: -float(x.average_mark))

    return [student.name for student in sorted_students_by_marks][:number_of_top_students]


# 4.3.2
def sort_students_by_age(file_path):
    """writes CSV student information to the new file in descending order of age."""
    with open(os.path.join('data', file_path), 'r') as infile:
        header = next(infile)
        reader = csv.reader(infile)

        students = [Student(row[0], row[1], row[2]) for row in reader]

    sorted_by_age = sorted(students, key=lambda x: -int(x.age))

    with open(os.path.join('data', 'students_sorted_by_age.csv'), 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(tuple(header.strip().split(',')))
        writer.writerows([(st.name, st.age, st.average_mark) for st in sorted_by_age])


# 4.4.1
def calling_inner_function():
    """Calling inner function without moving it from inside of enclosed_function

    We need to add return inner function. Then we can call it:

    >>> calling_inner_function()
    I am local variable!
    """

    def enclosing_funcion():
        a = "I am variable from enclosed function!"

        def inner_function():

            a = "I am local variable!"
            print(a)
        return inner_function

    enclosing_funcion()()


# 4.4.2
a = "I am global variable!"


def calling_global_variable():
    """
    To call global 'a' we use global

    >>> calling_global_variable()
    I am global variable!
    """

    def enclosing_funcion():
        a = "I am variable from enclosed function!"

        def inner_function():

            global a  # modified string
            print(a)
        return inner_function

    enclosing_funcion()()


# 4.4.3
a = "I am global variable!"


def calling_enclosed_variable():
    """
    To call enclosed 'a' we use nonlocal

    >>> calling_enclosed_variable()
    I am variable from enclosed function!
    """

    def enclosing_funcion():
        a = "I am variable from enclosed function!"

        def inner_function():

            nonlocal a  # modified string
            print(a)
        return inner_function

    enclosing_funcion()()


# 4.5
def remember_result(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print(f"Last Result = {inner.result}")
        inner.result = func(*args, **kwargs)
    inner.result = None
    return inner


@remember_result
def sum_list(*args):
    """
    Implement a decorator remember_result which remembers last result of function it decorates
    and prints it before next call.

    >>> sum_list("a", "b")
    Last Result = None
    Current result = 'ab'

    >>> sum_list("abc", "cde")
    Last Result = ab
    Current result = 'abccde'

    >>> sum_list(3, 4, 5)
    Last Result = abccde
    Current result = '12'
    """
    result = "" if type(args[0]) == str else 0
    for item in args:
        result += item
    print(f"Current result = '{result}'")
    return result


# 4.6
def call_once(func):
    """
    Decorator which runs a function or method once
    """
    @wraps(func)
    def inner(*args, **kwargs):
        if not inner.called:
            result = func(*args, **kwargs)
            inner.called = True
            return result
    inner.called = False
    return inner


@call_once
def sum_of_numbers(a, b):
    """

    >>> sum_of_numbers(1, 4)
    5
    >>> sum_of_numbers(11, 4)

    >>> sum_of_numbers(11, 4)

    """
    return a + b


# 4.7
"""
Module a imports module c that defines variable x = 5.
Then module a imports module b that imports module c and redefines it's
global variable x to 42.
After that module a call module's c global variable x that equal to 42 and
prints it.
"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
