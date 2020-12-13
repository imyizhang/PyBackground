#!/usr/bin/env python
# -*- coding: utf-8 -*-

TIMEOUT = 3

import functools


# task class as decorator
class task(object):

    def __init__(self, scheduler, timeout=TIMEOUT):
        self.scheduler = scheduler
        self.timeout = timeout

    def __call__(self, fn):
        @functools.wraps(fn)
        def start(*args, **kwargs):
            return self.scheduler.start(fn, args=args, kwargs=kwargs, timeout=self.timeout)
        fn.start = start
        return fn
