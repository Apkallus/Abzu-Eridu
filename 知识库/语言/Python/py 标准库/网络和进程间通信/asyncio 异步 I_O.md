#  asyncio --- 异步 I/O

https://docs.python.org/zh-cn/3.14/library/asyncio.html

## 运行器

https://docs.python.org/zh-cn/3.14/library/asyncio-runner.html

### 运行 asyncio 程序

#### `asyncio.run`

```python
asyncio.run(coro, *, debug=None, loop_factory=None)
```

在 asyncio 事件循环中执行 `coro` 并返回结果。

参数可以是任意可等待对象。

此函数会运行该可等待对象，负责管理 asyncio 事件循环，*终结化异步生成器*，并关闭执行器。

当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用。

如果 `debug` 为 `True`，事件循环将运行于调试模式。`False` 将显式地禁用调试模式。使用 `None` 将沿用全局调试模式设置。

如果 `loop_factory` 不为 `None`，它将被用来创建一个新的事件循环；否则将会使用 `asyncio.new_event_loop()`。最终该循环将被关闭。此函数应当被用作 asyncio 程序的主入口点，在理想情况下应当只被调用一次。建议使用 `loop_factory` 来配置事件循环而不是使用策略。传入 `asyncio.EventLoop` 将允许不带策略系统地运行 asyncio。

执行器的关闭有 5 分钟的超时限制。如果执行器未在时限之内结束，将发出警告消息并关闭执行器。

示例：

```python
async def main():
    await asyncio.sleep(1)
    print('hello')

asyncio.run(main())
```

在 3.7 版本新增。

在 3.9 版本发生变更：更新为使用 `loop.shutdown_default_executor()`。

在 3.10 版本发生变更：默认情况下 `debug` 为 `None` 即沿用全局调试模式设置。

在 3.12 版本发生变更：增加了 `loop_factory` 形参。

在 3.14 版本发生变更：`coro` 可以是任意可等待对象。

> **备注**
> `asyncio` 策略系统已弃用，将在 Python 3.16 中删除；从那时起，需要显式的 `loop_factory` 来配置事件循环。