def f(a, b=1):
    pass

print(f.__defaults__)#使用__code__#总参数个数

print(f.__code__.co_argcount)#总参数名

print(f.__code__.co_varnames)

import inspect

i = inspect.getfullargspec(f)

print(i.args)
