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

Use `@task` to define your function and start executing it, `now(cost)` as an example:

```python
import pybackground

sched = pybackground.BackgroundScheduler()


import time

@task(sched)
def now(cost=3):
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()) )
    time.sleep(cost)
    
now.sched()
```



## Related Projects

* [APScheduler](https://github.com/agronholm/apscheduler) ([apscheduler.readthedocs.org](http://apscheduler.readthedocs.org))