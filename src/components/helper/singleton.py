"""This module contain class representing singleton pattern for further implementation"""


class Singleton(object):
    """
        This module contain class representing singleton pattern for further implementation

        Attributes:
            _instance attribute contains sole instance of class
    """

    _instance = None

    def __new__(class_, *args, **kwargs):
        """rewrite __new__ for preventing creating new instances of class"""
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)

        return class_._instance
