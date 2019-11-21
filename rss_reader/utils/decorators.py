from functools import wraps


def call_save_news_after_method(method):
    """Decorator for methods of class RssInterfase

    Calls method to store news. You can apply it to
    print_news method or to_json method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        output = method(self, *args, **kwargs)
        self._store_news()
        return output
    return wrapper
