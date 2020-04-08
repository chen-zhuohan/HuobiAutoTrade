import functools
import sys
import time
import traceback

from common.instance import log
from common.email_helper import send_error


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


logger = Logger('one more try')


def one_more_try(message: str, max=3, important=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info('one more try has in work, the one more try function: {}'.format(func))
            error = None
            for i in range(max):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error = e
                    logger.info('one more try wrong, detail: {}, retry time: {}'.format(e.args, i))
                    time.sleep(0.1)
                    if important:
                        send_error(e, message)
            logger.info('one more try wrong complete wrong')
            send_error(error, message)
            traceback.print_exc(file=sys.stdout)
            raise error
        return wrapper
    return decorator