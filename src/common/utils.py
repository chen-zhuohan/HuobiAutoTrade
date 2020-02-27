import functools
import time

from common.instance import log
from src.common.email_helper import send_error


def one_more_try(message, max=3, important=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    time.sleep(0.1)
                    if important:
                        send_error(e, message)
            send_error(e, message)
            raise e
        return wrapper
    return decorator


class Logger:
    def __init__(self, tag: str = 'LOGGING', clue: str = None):
        self._tag = tag
        self._clue = clue
        self.prefix = None

        self.make_prefix()

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value
        self.make_prefix()

    @property
    def clue(self):
        return self._clue

    @clue.setter
    def clue(self, value):
        self._clue = value
        self.make_prefix()

    def make_prefix(self):
        prefix = '[{}]'.format(self._tag.upper())
        if self._clue:
            prefix = '{}[{}]'.format(prefix, self._clue)
        self.prefix = prefix

    def _make_log(self, msg):
        log_ = '{} {}'.format(self.prefix, msg)
        return log_

    def debug(self, msg):
        log.debug(self._make_log(msg))

    def info(self, msg):
        log.info(self._make_log(msg))

    def warning(self, msg):
        log.warning(self._make_log(msg))

    def error(self, msg):
        log.error(self._make_log(msg))