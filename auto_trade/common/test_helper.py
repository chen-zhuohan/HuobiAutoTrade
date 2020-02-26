import sys
import traceback


def format_print_error(e: Exception):
    print('--------------------------------' * 3)
    print('Get Exception in web try : {}'.format(e))
    print('--------------------------------' * 3)
    traceback.print_exc(file=sys.stdout)
    print('--------------------------------' * 3)


def try_and_except(func):
    try:
        assert func
    except AssertionError as e:
        format_print_error(e)


def assertFalse(a: bool):
    try_and_except(lambda: a is False)
    # try:
    #     assert a is False
    # except AssertionError as e:
    #     format_print_error(e)


# if __name__ == '__main__':
assertFalse(True)