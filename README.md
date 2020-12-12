# PyBackground

PyBackground is

* a lightweight scheduler that runs in the background
* written in [Python (3.7+) Standard Library](https://docs.python.org/3.7/library/)



PyBackground supports to

* execute tasks using thread pool
* run in the either foreground or background
* use `@task` decorator to define task



## Quickstart

Define your function, `now(cost)` as an example:

```python
import time

def now(cost=1):
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()) )
    time.sleep(cost)
```

Create a PyBackground scheduler and start executing your function:

```python
import pybackground

sched = pybackground.BackgroundScheduler()
sched.start(now)
```

Shutdown the scheduler:

```python
sched.shutdown()
```



### Handle with the infinite loops

Let's work based on `now(cost)` as an example:

```python
import pybackground

sched = pybackground.BackgroundScheduler()
print(sched.stopped)

def timer(interval=5):
    while not sched.stopped:
        now()

sched.start(timer)
```

`timer(interval)` then runs forever in a seperate thread. When you'd like to terminate it, shutdown the scheduler as usual:

```python
sched.shutdown()
```



### Play with the `@task` decorator

Use `@task` decorator to define your function and start executing it, `now(cost)` as an example:

```python
import pybackground

sched = pybackground.BackgroundScheduler()


import time

@pybackground.task(sched)
def now(cost=3):
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()) )
    time.sleep(cost)

now.sched()
```



## Documentation

### `BackgroundScheduler`/`BlockingScheduler`

```python
class pybackground.BackgroundScheduler/BlockingScheduler(max_worker=<num_cpu_cores>)
```

`max_worker` is set for `ThreadPoolExecutor`, default value is the number of CPU cores.

* `stopped`

  The scheduler is stopped or not, `True` (default) or `False`.

* `start(fn, args=(), kwargs={}, timeout=TIMEOUT)`

  Let scheduler start executing your function using thread pool in the background or foreground, default value of `timeout` is `TIMEOUT`, 3 seconds.

* `shutdown(wait=True)`

  Shutdown the scheduler.



### `task`

```python
class pybackground.task(scheduler, timeout=TIMEOUT)
```

`timeout` is set for function executing, default value is `TIMEOUT`, 3 seconds.

* Use `@task` decorator to define your function and start executing it:

  ```python
  @task(scheduler)
  def fn(args, kwargs):
      pass
    
  fn.shed(*args, **kwargs)
  ```

  `fn.shed(*args, **kwargs)` is equivaluent to `sheduler.start(fn, args, kwargs)` with normal function definition.



## Related Projects

* [APScheduler](https://github.com/agronholm/apscheduler) ([apscheduler.readthedocs.org](http://apscheduler.readthedocs.org))

