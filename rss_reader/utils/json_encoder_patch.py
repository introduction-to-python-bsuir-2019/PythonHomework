"""Module to implement storing custom classes via Json and pickle"""

from json import JSONEncoder
import pickle


class PythonObjectEncoder(JSONEncoder):
    """Json encoder class to store NEWS class as json via pickle"""
    def default(self, obj):
        return {'_python_object': pickle.dumps(obj).decode('latin1')}


def as_python_object(dct):
    """Loads stored NEWS objects as python NEWS object"""
    try:
        return pickle.loads(dct['_python_object'].encode('latin1'))
    except KeyError:
        return dct
