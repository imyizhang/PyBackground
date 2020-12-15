# PyBackground

PyBackground is

* a lightweight scheduler that runs tasks in the background
* written in [Python (3.7+) Standard Library](https://docs.python.org/3.7/library/)



PyBackground supports to

* execute tasks using thread pool
* run in the background (or foreground)
* use `@task` decorator to define task



## Quickstart

Define your functions:

```python
import time

def now(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()) )
    
def utcnow(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime()) )
```

Create a PyBackground scheduler and start executing your functions:

```python
import pybackground

sched = pybackground.BackgroundScheduler()
sched.start(now, args=(1,))
sched.start(utcnow, args=(1,))
```

Shutdown the scheduler:

```python
sched.shutdown(wait=True)
```



### Handle with the infinite loops

Let's work based on `now(cost)` as an example:

```python
import pybackground

sched = pybackground.BackgroundScheduler()
print(sched.stopped)

def timer(interval=3):
    while not sched.stopped:
        now()

sched.start(timer, args=(3,))
```

`timer(interval)` then runs forever in a seperate thread. When you'd like to terminate it, shutdown the scheduler as usual:

```python
sched.shutdown(wait=True)
```



### Play with the `@task` decorator

Use `@task` decorator to define your functions and start executing them, scheduling `now(cost)` and `utcnow(cost)` as an example:

```python
import pybackground

sched = pybackground.BackgroundScheduler()

import time

@pybackground.task(sched)
def now(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()) )
    
now.start(cost=1)

@pybackground.task(sched)
def utcnow(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime()) )
    
utcnow.start(cost=1)
```

Shutdown the scheduler in normal way:

```python
sched.shutdown(wait=True)
```



### Install PyBackground

```bash
$ pip install pybackground
```



## Documentation

### `BackgroundScheduler`/`BlockingScheduler`

```python
class pybackground.BackgroundScheduler/BlockingScheduler(max_worker=<num_cpu_cores>)
```

`max_worker` is set for `ThreadPoolExecutor`, default value is the number of CPU cores.

* `stopped`

  The scheduler is stopped or not, `True` (default) or `False`.

* `latest_id`

  The latest task id, which may be useful for `pybackground.BlockingScheduler`. 

* `task`

  The task id, `Task` object (`collections.namedtuple('Task', 'fn, args, kwargs')`) dictionary, `{}` as default.

* `future`

  The task id, [`Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object dictionary, `{}` as default.

* `start(fn, args=(), kwargs={})`

  Let scheduler start executing your function using thread pool in the background (or foreground). It returns corresponding task id.

* `shutdown(wait=True)`

  Shutdown the scheduler.



### `task`

```python
class pybackground.task(scheduler)
```

* Use `@task` decorator to define your functions and start executing them:

  ```python
  @task(scheduler)
  def fn(args, kwargs):
      pass
    
  fn.start(*args, **kwargs)
  ```

  `fn.start(*args, **kwargs)` is equivaluent to `sheduler.start(fn, args, kwargs)` using normal function definition.



## Related Projects

* [APScheduler](https://github.com/agronholm/apscheduler) ([apscheduler.readthedocs.org](http://apscheduler.readthedocs.org))

