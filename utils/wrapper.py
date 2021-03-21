# -*- coding: utf-8 -*-
"""
一些装饰器
"""

import time
import traceback
from functools import wraps
from inspect import signature


def debug(log=print, ignore_exception=False):
    """
    当函数发生异常时，记录详细的异常信息。
      - `log`：记录异常信息的函数名。
      - `ignore_exception`：是否抛出该异常。
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
if __name__ == "__main__":
    @debug(print)
    def fun1(*args, **kwargs):
        print(*args, **kwargs)
        raise RuntimeError("testing...")

    fun1(1, 2, "hello")


def retry(n=-1, interval=0, log=print):
    """
    当函数发生异常时，重复执行函数。
      - `n`：当函数发生异常时，最多重复执行n次。执行n次之后会抛出异常。
        n为负数时，重复执行无限次。
      - `interval`：每次重复执行的间隔时间。
      - `log`：记录异常信息的函数名。
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
if __name__ == "__main__":
    @retry(5, interval=1)
    def fun2(*args, **kwargs):
        print(*args, **kwargs)
        raise RuntimeError("testing...")

    fun2(1, 2, "hello")


def validator(*types, **kwtypes):
    """ 对函数收到的实参进行类型检查。 """
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
if __name__ == "__main__":
    @validator(int, (str, bytes))
    def fun3(x, y, *args, **kwargs):
        print(*args, **kwargs)

    fun3("", 2, "hello")
    fun3(1, 2, "hello")
    fun3(1, "", "hello")
