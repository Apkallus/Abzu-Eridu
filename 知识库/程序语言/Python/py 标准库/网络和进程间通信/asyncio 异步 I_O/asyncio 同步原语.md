# 同步原语

**源代码：** [Lib/asyncio/locks.py](https://github.com/python/cpython/tree/3.15/Lib/asyncio/locks.py)

---

`asyncio` 同步原语的设计与 [`threading`] 模块中的同步原语类似，但有两个重要注意事项：

- `asyncio` 原语不是线程安全的，因此不应将其用于操作系统线程同步（该场景请使用 [`threading`]）；
- 这些同步原语的方法不接受 `timeout` 参数；请使用 [`asyncio.wait_for()`] 函数执行带超时的操作。

`asyncio` 具有以下基本同步原语：

- [`Lock`]
- [`Event`]
- [`Condition`]
- [`Semaphore`]
- [`BoundedSemaphore`]
- [`Barrier`]

---

## Lock

### `class asyncio.Lock`

实现用于 `asyncio` 任务的互斥锁。不是线程安全的。

`asyncio` 锁可用于保证对共享资源的独占访问。

使用 `Lock` 的首选方式是 [`async with`] 语句：

```py
lock = asyncio.Lock()

# ... 稍后
async with lock:
    # 访问共享状态
```

这等价于：

```py
lock = asyncio.Lock()

# ... 稍后
await lock.acquire()
try:
    # 访问共享状态
finally:
    lock.release()
```

在 3.10 版更改：移除了 `loop` 参数。

#### `async acquire()`

获取锁。

此方法会等待锁变为 *unlocked*，将其设置为 *locked* 并返回 `True`。

当有多个协程阻塞在 `acquire()` 中等待锁被解锁时，最终只有一个协程会继续执行。

获取锁是 *公平* 的：继续执行的协程将是最先开始等待该锁的协程。

#### `release()`

释放锁。

当锁处于 *locked* 状态时，将其重置为 *unlocked* 并返回。

如果锁处于 *unlocked* 状态，则引发 [`RuntimeError`]。

#### `locked()`

如果锁处于 *locked* 状态，则返回 `True`。

## Event

### `class asyncio.Event`

事件对象。不是线程安全的。

`asyncio` 事件可用于通知多个 `asyncio` 任务某个事件已经发生。

`Event` 对象管理一个内部标志，可通过 [`set()`] 方法将其设置为 *true*，并通过 [`clear()`] 方法重置为 *false*。[`wait()`] 方法会阻塞，直到该标志被设置为 *true*。该标志初始为 *false*。

在 3.10 版更改：移除了 `loop` 参数。

示例：

```py
async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def main():
    # 创建一个 Event 对象。
    event = asyncio.Event()

    # 创建一个 Task，等待 'event' 被设置。
    waiter_task = asyncio.create_task(waiter(event))

    # 休眠 1 秒并设置事件。
    await asyncio.sleep(1)
    event.set()

    # 等待 waiter 任务完成。
    await waiter_task

asyncio.run(main())
```

#### `async wait()`

等待事件被设置。

如果事件已设置，立即返回 `True`。否则阻塞，直到另一个任务调用 [`set()`]。

#### `set()`

设置事件。

所有等待事件被设置的任务将立即被唤醒。

#### `clear()`

清除（取消设置）事件。

之后等待 [`wait()`] 的任务将阻塞，直到再次调用 [`set()`] 方法。

#### `is_set()`

如果事件已设置，则返回 `True`。

## Condition

### `class asyncio.Condition()`

```py
class asyncio.Condition(lock=None)
```

条件对象。不是线程安全的。

`asyncio` 条件原语可供任务等待某个事件发生，然后获取对共享资源的独占访问。

本质上，`Condition` 对象结合了 [`Event`] 和 [`Lock`] 的功能。可以让多个 `Condition` 对象共享一个 `Lock`，从而在不同任务之间协调对共享资源的独占访问，这些任务关心该共享资源的特定状态。

可选的 `lock` 参数必须是 [`Lock`] 对象或 `None`。在后一种情况下，会自动创建一个新的 `Lock` 对象。

在 3.10 版更改：移除了 `loop` 参数。

使用 `Condition` 的首选方式是 [`async with`] 语句：

```py
cond = asyncio.Condition()

# ... 稍后
async with cond:
    await cond.wait()
```

这等价于：

```py
cond = asyncio.Condition()

# ... 稍后
await cond.acquire()
try:
    await cond.wait()
finally:
    cond.release()
```

#### `async acquire()`

获取底层锁。

此方法会等待底层锁变为 *unlocked*，将其设置为 *locked* 并返回 `True`。

#### `notify()`

```py
notify(n=1)
```

唤醒 `n` 个（默认为 1 个）正在等待此条件的任务。如果等待的任务少于 `n` 个，则全部唤醒。

调用此方法前必须已获取锁，并在调用后尽快释放。如果在锁处于 *unlocked* 状态时调用，则引发 [`RuntimeError`] 错误。

#### `locked()`

如果底层锁已被获取，则返回 `True`。

#### `notify_all()`

唤醒所有正在等待此条件的任务。

此方法类似于 [`notify()`]，但会唤醒所有等待任务。

调用此方法前必须已获取锁，并在调用后尽快释放。如果在锁处于 *unlocked* 状态时调用，则引发 [`RuntimeError`] 错误。

#### `release()`

释放底层锁。

在未锁定的锁上调用时，会引发 [`RuntimeError`]。

#### `async wait()`

等待直到被通知。

如果调用此方法时调用任务尚未获取锁，则引发 [`RuntimeError`]。

此方法会释放底层锁，然后阻塞，直到被 [`notify()`] 或 [`notify_all()`] 调用唤醒。一旦被唤醒，`Condition` 会重新获取其锁，此方法返回 `True`。

注意，任务 *可能* 从此调用中虚假返回，因此调用方应始终重新检查状态，并准备好再次 `wait()`。因此，你可能更愿意使用 [`wait_for()`]。

#### `async wait_for()`

```py
async wait_for(predicate)
```

等待直到谓词变为 *true*。

谓词必须是可调用对象，其结果将被解释为布尔值。此方法会重复 [`wait()`]，直到谓词求值为 *true*。最终值就是返回值。

## Semaphore

### `class asyncio.Semaphore()`

```py
class asyncio.Semaphore(value=1)
```

信号量对象。不是线程安全的。

信号量管理一个内部计数器，每次调用 [`acquire()`] 时递减，每次调用 [`release()`] 时递增。计数器永远不会低于零；当 `acquire()` 发现它为零时，会阻塞，等待某个任务调用 `release()`。

可选的 `value` 参数给出内部计数器的初始值（默认为 `1`）。如果给定值小于 `0`，则引发 [`ValueError`]。

在 3.10 版更改：移除了 `loop` 参数。

使用 `Semaphore` 的首选方式是 [`async with`] 语句：

```py
sem = asyncio.Semaphore(10)

# ... 稍后
async with sem:
    # 使用共享资源
```

这等价于：

```py
sem = asyncio.Semaphore(10)

# ... 稍后
await sem.acquire()
try:
    # 使用共享资源
finally:
    sem.release()
```

#### `async acquire()`

获取信号量。

如果内部计数器大于零，则将其减一并立即返回 `True`。如果为零，则等待直到调用 [`release()`]，然后返回 `True`。

#### `locked()`

如果无法立即获取信号量，则返回 `True`。

#### `release()`

释放信号量，将内部计数器加一。可以唤醒一个正在等待获取信号量的任务。

与 [`BoundedSemaphore`] 不同，`Semaphore` 允许 `release()` 调用次数多于 `acquire()` 调用次数。

## BoundedSemaphore

### `class asyncio.BoundedSemaphore()`

```py
class asyncio.BoundedSemaphore(value=1)
```

有界信号量对象。不是线程安全的。

有界信号量是 [`Semaphore`] 的一个版本，如果 [`release()`] 将内部计数器增加到超过初始 `value`，则会引发 [`ValueError`]。

在 3.10 版更改：移除了 `loop` 参数。

## Barrier

### `class asyncio.Barrier()`

```py
class asyncio.Barrier(parties)
```

屏障对象。不是线程安全的。

屏障是一种简单的同步原语，允许阻塞，直到有 `parties` 个任务在等待它。任务可以在 [`wait()`] 方法上等待，并会被阻塞，直到指定数量的任务最终都在 `wait()` 上等待。此时，所有等待任务将同时解除阻塞。

[`async with`] 可用作等待 [`wait()`] 的替代方式。

屏障可以重复使用任意次数。

示例：

```py
async def example_barrier():
   # 包含 3 个参与方的屏障
   b = asyncio.Barrier(3)

   # 创建 2 个新的等待任务
   asyncio.create_task(b.wait())
   asyncio.create_task(b.wait())

   await asyncio.sleep(0)
   print(b)

   # 第三次 .wait() 调用通过屏障
   await b.wait()
   print(b)
   print("barrier passed")

   await asyncio.sleep(0)
   print(b)

asyncio.run(example_barrier())
```

此示例的结果为：

```text
<asyncio.locks.Barrier object at 0x... [filling, waiters:2/3]>
<asyncio.locks.Barrier object at 0x... [draining, waiters:0/3]>
barrier passed
<asyncio.locks.Barrier object at 0x... [filling, waiters:0/3]>
```

在 3.11 版添加。

#### `async wait()`

通过屏障。当所有参与屏障的任务都调用了此函数后，它们会同时解除阻塞。

当屏障中正在等待或阻塞的任务被取消时，该任务会退出屏障，屏障保持相同状态。如果屏障状态为 `filling`，则等待任务数减 1。

返回值是 0 到 `parties-1` 范围内的整数，每个任务不同。这可用于选择一个任务执行某些特殊清理工作，例如：

```py
...
async with barrier as position:
   if position == 0:
      # 只有一个任务会打印此内容
      print('End of *draining phase*')
```

如果屏障在任务等待时被破坏或重置，此方法可能引发 [`BrokenBarrierError`] 异常。如果任务被取消，则可能引发 [`CancelledError`]。

#### `async reset()`

将屏障恢复为默认的空状态。任何正在等待它的任务都将收到 [`BrokenBarrierError`] 异常。

如果屏障已损坏，可能最好直接放弃它并创建一个新的屏障。

#### `async abort()`

将屏障置于损坏状态。这会导致任何当前或未来的 [`wait()`] 调用失败，并引发 [`BrokenBarrierError`]。例如，如果某个任务需要中止，可使用此方法，以避免任务无限等待。

#### `parties`

通过屏障所需的任务数。

#### `n_waiting`

在填充状态下当前正在屏障中等待的任务数。

#### `broken`

一个布尔值，如果屏障处于损坏状态，则为 `True`。

### `exception asyncio.BrokenBarrierError`

此异常是 [`RuntimeError`] 的子类，在 [`Barrier`] 对象被重置或损坏时引发。

---

在 3.9 版更改：移除了使用 `await lock` 或 `yield from lock` 获取锁，和/或使用 [`with`] 语句（`with await lock`、`with (yield from lock)`）的方式。请改用 `async with lock`。