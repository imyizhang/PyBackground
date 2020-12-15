#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Schedulers that run tasks with ThreadPoolExecutor in the foreground or background,
BlockingScheduler, BackgroundScheduler.
"""

TIMEOUT = 3

import collections
import abc
import os
import concurrent.futures
import threading
import uuid


Task = collections.namedtuple('Task', 'fn, args, kwargs')


class Scheduler(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, max_workers=os.cpu_count()):
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.RLock()
        self._stopped = True
        self._id = None
        self._task = []
        self._future = []

    @property
    def stopped(self):
        return self._stopped

    # useful for BlockingScheduler
    @property
    def latest_id(self):
        return self._id

    @property
    def task(self):
        return dict(self._task)

    @property
    def future(self):
        return dict(self._future)

    # cannot start new tasks after shutdown
    @abc.abstractmethod
    def start(self, fn, args=(), kwargs={}):
        self._stopped = False
        self._id = uuid.uuid4().hex
        self._packup(fn, args, kwargs)
        with self._lock:
            self._run(fn, args, kwargs)

    def _packup(self, fn, args, kwargs):
        self._task.append( (self._id, Task(fn, args, kwargs)) )

    def _run(self, fn, args, kwargs):
        future = self._executor.submit(fn, *args, **kwargs)
        self._future.append( (self._id, future) )

    @abc.abstractmethod
    def shutdown(self, wait=True):
        self._stopped = True
        with self._lock:
            self._executor.shutdown(wait=wait)


class BlockingScheduler(Scheduler):
    """A scheduler that runs in the foreground.
    BlockingScheduler.start(fn, args, kwargs) will block.
    """

    _event = None

    def start(self, fn, args=(), kwargs={}):
        self._event = threading.Event()
        super().start(fn, args, kwargs)
        self._loop(TIMEOUT)
        return self._id

    def _loop(self, timeout):
        while not self.stopped:
            self._event.wait(timeout=timeout)
            self._event.clear()

    def shutdown(self, wait=True):
        super().shutdown(wait)
        self._event.set()


class BackgroundScheduler(BlockingScheduler):
    """A scheduler that runs in the background using a separate thread.
    BackgroundScheduler.start(fn, args, kwargs) will return immediately.
    """

    _thread = None

    def start(self, fn, args=(), kwargs={}):
        self._event = threading.Event()
        Scheduler.start(self, fn, args, kwargs)
        self._thread = threading.Thread(target=self._loop, name='background', args=(TIMEOUT,))
        self._thread.daemon = True
        self._thread.start()
        return self._id

    def shutdown(self, wait=True):
        super().shutdown(wait)
        self._thread.join()
        del self._thread
