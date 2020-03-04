

def get_func_args(f) -> tuple:
    return f.__code__.co_varnames

# def get_func_args(f) -> list:
#     import inspect
#     i = inspect.getfullargspec(f)
#     return i.args
