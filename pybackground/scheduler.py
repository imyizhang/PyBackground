#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Schedulers that run tasks with ThreadPoolExecutor in the foreground or background,
BlockingScheduler, BackgroundScheduler.
"""

TIMEOUT = 3

import functools


# task class as decorator
class task(object):

    def __init__(self, scheduler, timeout=TIMEOUT):
        self.scheduler = scheduler
        self.timeout = timeout

    def __call__(self, fn):
        @functools.wraps(fn)
        def sched(*args, **kwargs):
            self.scheduler.start(fn, args=args, kwargs=kwargs, timeout=self.timeout)
        fn.sched = sched
        return fn


import os, threading, concurrent.futures


class Scheduler(object):

    def __init__(self, max_workers=os.cpu_count()):
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.RLock()
        self.stopped = True

    # cannot start new tasks after shutdown
    def start(self, fn, args=(), kwargs={}):
        self.stopped = False
        with self._lock:
            self._run(fn, args, kwargs)

    def _run(self, fn, args, kwargs):
        future = self._executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True):
        self.stopped = True
        with self._lock:
            self._executor.shutdown(wait=wait)


class BlockingScheduler(Scheduler):
    """A scheduler that runs in the foreground.
    Scheduler.start(fn, args, kwargs) will block.
    """

    _event = None

    def start(self, fn, args=(), kwargs={}, timeout=TIMEOUT):
        self._event = threading.Event()
        super(BlockingScheduler, self).start(fn, args, kwargs)
        self._loop(timeout)

    def _loop(self, timeout):
        while not self.stopped:
            self._event.wait(timeout=timeout)
            self._event.clear()

    def shutdown(self, wait=True):
        super(BlockingScheduler, self).shutdown(wait)
        self._event.set()


class BackgroundScheduler(BlockingScheduler):
    """A scheduler that runs in the background using a separate thread.
    Scheduler.start(fn, args, kwargs) will return immediately.
    """

    _thread = None

    def start(self, fn, args=(), kwargs={}, timeout=TIMEOUT):
        self._event = threading.Event()
        Scheduler.start(self, fn, args, kwargs)
        self._thread = threading.Thread(target=self._loop, name='background', args=(timeout,))
        self._thread.daemon = True
        self._thread.start()

    def shutdown(self, wait=True):
        super(BackgroundScheduler, self).shutdown(wait)
        self._thread.join()
        del self._thread
