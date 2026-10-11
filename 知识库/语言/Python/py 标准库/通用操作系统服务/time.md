# time --- 时间的访问和转换

https://docs.python.org/zh-cn/3.14/library/time.html

## 函数

- `time.localtime()`
    时间元组
- `time.strftime("%Y-%m-%d %H:%M:%S", 时间元组)`
    格式化时间字符串


### ♾️ `time.sleep`

```python
time.sleep(seconds, /)
```

暂停调用线程的执行，持续给定的秒数。参数可以是非整数，以表示更精确的睡眠时间。

> 常用来简单阻塞代码执行：不精确的等待事件发生，或在循环中用来定时执行

如果睡眠被信号中断，且信号处理程序未引发异常，则会以重新计算的超时时间重新开始睡眠。

由于系统中其他活动的调度，暂停时间可能会比请求的时间长任意量。

**Windows 实现**

在 Windows 上，如果 *seconds* 为零，线程会将剩余时间片让给任何其他准备运行的线程。如果没有其他准备运行的线程，该函数会立即返回，线程继续执行。在 Windows 10 及更新版本上，实现使用[高分辨率定时器](https://learn.microsoft.com/windows/win32/api/synchapi/nf-synchapi-createwaitabletimerexw)，提供 100 纳秒的分辨率。如果 *seconds* 为零，则使用 `Sleep(0)`。

**Unix 实现**

- 如果可用，使用 `clock_nanosleep()`（分辨率：1 纳秒）；
- 或如果可用，使用 `nanosleep()`（分辨率：1 纳秒）；
- 或使用 `select()`（分辨率：1 微秒）。

> **注意**
> 要模拟“空操作”，请使用 `pass` 而不是 `time.sleep(0)`。
>
> 要主动让出 CPU，请指定实时调度策略，并使用 `os.sched_yield()` 代替。

引发一个审计事件 `time.sleep`，参数为 `seconds`。

在 3.5 版本发生变更：即使睡眠被信号中断，该函数现在也会至少睡眠 *seconds*，除非信号处理程序引发异常（参见 [PEP 475](https://peps.python.org/pep-0475/) 了解理由）。

在 3.11 版本发生变更：在 Unix 上，如果可用，现在使用 `clock_nanosleep()` 和 `nanosleep()` 函数。在 Windows 上，现在使用可等待定时器。

在 3.13 版本发生变更：引发审计事件。

在 3.15 版本发生变更：接受任何实数，而不仅是整数或浮点数。