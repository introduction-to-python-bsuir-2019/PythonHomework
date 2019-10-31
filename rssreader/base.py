"""Module to store base objects of the application"""


class BaseClass:
    """Base class to be used as parent for all classes. Only __repr__ method is implemented."""
    def __repr__(self) -> str:
        """Return all instance attributes"""
        return ', '.join("%s: %r" % item for item in vars(self).items())
