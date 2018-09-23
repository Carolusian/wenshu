#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File: wenshu/utils.py
# Author: Carolusian <https://github.com/carolusian>
# Date: 23.09.2018
# Last Modified Date: 23.09.2018
#
# Copyright 2018 Carolusian
import time
import functools
from .config import get_logger


logger = get_logger(__name__)


def retry(times=3, delay=5, allowed_exceptions=()):
    def wrapper(func):
        """Wrapper passes `func` to functools.wraps"""
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            """Decorator function to be returned"""
            for _ in range(times):
                try:
                    # Just return the function result when no exception occurs
                    result = func(*args, **kwargs)
                    return result
                except allowed_exceptions as ex:
                    pass
                logger.info('Wait for %s seconds to retry...' % delay)
                time.sleep(delay)
        return decorator
    return wrapper
