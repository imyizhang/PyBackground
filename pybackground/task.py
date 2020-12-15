#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools


# task class as decorator
class task(object):

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def __call__(self, fn):
        @functools.wraps(fn)
        def start(*args, **kwargs):
            return self.scheduler.start(fn, args=args, kwargs=kwargs)
        fn.start = start
        return fn
