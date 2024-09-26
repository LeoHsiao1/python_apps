""" Contains some decorators. """
import time
import traceback
from functools import wraps
from inspect import signature


def debug(log=print, ignore_exception=False):
    """
    Log detailed exception when an exception occurs.
    - `log`: A function used to log exception.
    - `ignore_exception`: Whether to throw the exception.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                log(traceback.format_exc())
                if not ignore_exception:
                    raise
        return wrapper
    return decorator


# sample
if __name__ == '__main__':
    @debug(print)
    def fun1(*args, **kwargs):
        print(*args, **kwargs)
        raise RuntimeError('testing...')

    fun1(1, 2, 'hello')


def retry(n=-1, interval=0, log=print):
    """
    Execute a function repeatedly when an exception occurs.
    - `n`: Retry up to n times, then throw the exception.
           If n is negative, it's unlimited.
    - `interval`: The interval between each retry.
    - `log`: A function used to log exception.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _n = n
            while 1:
                try:
                    return func(*args, **kwargs)
                except:
                    log(traceback.format_exc())
                    _n -= 1
                    if _n != 0:
                        time.sleep(interval)
                        continue
                    else:
                        raise
        return wrapper
    return decorator


# sample
if __name__ == '__main__':
    @retry(5, interval=1)
    def fun2(*args, **kwargs):
        print(*args, **kwargs)
        raise RuntimeError('testing...')

    fun2(1, 2, 'hello')


def validator(*types, **kwtypes):
    """ Checks the type of arguments the function receives. """
    def decorate(func):
        sign = signature(func)
        required_types = sign.bind_partial(*types, **kwtypes).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            actual_values = sign.bind(*args, **kwargs).arguments
            for k, v in actual_values.items():
                if k in required_types:
                    _type = required_types[k]
                    if not isinstance(v, _type):
                        raise TypeError("{}'s argument '{}' should be {}, but got {}.".format(
                            func, k, _type, type(v)))
            return func(*args, **kwargs)
        return wrapper

    return decorate


# sample
if __name__ == '__main__':
    @validator(int, (str, bytes))
    def fun3(x, y, *args, **kwargs):
        print(*args, **kwargs)

    fun3('' , 2 , 'hello')
    fun3(1  , 2 , 'hello')
    fun3(1  , '', 'hello')
