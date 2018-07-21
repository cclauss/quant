# -*- coding: UTF-8 -*-
# ae.h - 2018/4/23
import functools
import traceback

from log.quant_logging import logger
import time


def exc_time(func):
    @functools.wraps(func)
    def fn(*args, **kv):
        start_time = time.time()
        tmp = func(*args, **kv)
        end_time = time.time()
        logger.debug("%s executed,  elapsed time: %.2f ms" % (func.__name__, (end_time - start_time) * 1000))
        return tmp

    return fn


def error_handler(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kv):
            try:
                return func(*args, **kv)
            except Exception as e:
                logger.error('%s failed, args: %s' % (func.__name__, args))
                logger.error(traceback.format_exc())
                return default

        return wrapper

    return decorator
