# `pwnlib.log` — 日志记录相关内容

用于在漏洞利用过程中以及 `pwntools` 内部打印状态的日志记录模块。

## 漏洞利用开发者

通过使用标准的 `from pwn import *`，一个名为 `log` 的对象会被插入全局命名空间。你可以使用它在漏洞利用过程中打印状态消息。

例如：

```py
log.info('Hello, world!')
```

会打印：

```log
[*] Hello, world!
```

此外，还有一些巧妙机制可用于对正在运行的任务执行状态更新（例如暴力破解时）：

```py
p = log.progress('Working')
p.status('Reticulating splines')
time.sleep(1)
p.success('Got a shell!')
```

日志的详细程度最容易通过设置全局 `context` 对象上的 `log_level` 来控制：

```py
log.info("No you see me")
context.log_level = 'error'
log.info("Now you don't")
```

此属性的目的是控制哪些内容打印到屏幕，而不是哪些内容被发出。这意味着你可以将所有日志事件放入日志文件，而只想在屏幕上看到其中一小部分。

## Pwnlib 开发者

可以通过以下方式将模块特定的记录器导入模块：

```py
from pwnlib.log import getLogger
log = getLogger(__name__)
```

这提供了一种简便方式，可通过编程方式或配置文件过滤日志以进行调试。

使用 `progress` 时，应使用 `with` 关键字管理作用域，以确保即使抛出异常，spinner 也会停止。

## 技术细节

假定你熟悉 [`logging`](https://docs.python.org/3/library/logging.html#module-logging) 模块。

会创建一个名为 `pwnlib` 的 pwnlib 根记录器，并为其安装自定义处理器和格式化器。处理器从 `context.log_level` 确定其日志级别。

理想情况下，`context.log_level` 应只影响处理器将发出哪些记录，以便例如记录到文件不会受其改变。但出于性能原因，在正常情况下记录所有内容并不可行。特别是 `pwnlib.tubes.tube` 内部存在紧密循环，我们希望能够在其中调试，但如果我们不是在调试它们，它们就不应该输出消息（即使输出到日志文件也不行）。因此，pwnlib 内部有几处地方，除非 `context.log_level` 设置为 `logging.DEBUG` 或更低，否则甚至不会发出记录。

由 `Progress` 和 `Logger` 对象创建的日志记录会在 `extra` 字段上设置 `'pwnlib_msgtype'`，以表明生成了哪种类型的消息。此信息由格式化器用于在消息前添加符号，例如 `'[+] '` 出现在 `'[+] got a shell!'` 中。

使用 `logging` 模块的标准格式化器时，此字段会被忽略。

进度记录器上的所有状态更新（不会因节流而被丢弃）都会导致创建一条日志记录。然后 `extra` 字段会携带对 `Progress` 记录器的引用，名称为 `'pwnlib_progress'`。

如果自定义处理器确定 `term.term_mode` 已启用，则其 `extra` 字段中包含 `'pwnlib_progress'` 的日志记录不会产生消息，而是会创建动画进度行（带有 spinner！）。注意，其他处理器仍会看到有意义的日志记录。

自定义处理器仅处理级别至少为 `context.log_level` 的日志记录。因此，例如如果 `'pwnlib.tubes.ssh'` 的级别设置为 `'DEBUG'`，除非 `context.log_level` 也设置为 `'DEBUG'`，否则不会显示额外输出。然而，其他处理器会看到 `'pwnlib.tubes.ssh'` 记录器生成的额外日志记录。

## `install_default_handler()`

实例化一个 `Handler` 和 `Formatter`，并将它们安装到 `pwnlib` 根记录器。此函数会在导入 `pwn` 时自动调用。

## `class pwnlib.log.Progress`

```py
class pwnlib.log.Progress(logger: Logger, msg: str, status: str, level: int, args: tuple[Any], kwargs: dict[str, Any])
```

用于生成与某个正在运行的任务关联的日志记录的进度记录器。实例可用作上下文管理器，退出时自动将运行任务声明为成功，抛出异常时声明为失败。在调用 `success()` 或 `failure()` 后，状态将无法再更新。

此类旨在内部使用。应使用 `Logger.progress()` 创建进度记录器。

### `Progress.__init__() -> None`

```py
Progress.__init__(logger: Logger, msg: str, status: str, level: int, args: tuple[Any], kwargs: dict[str, Any]) -> None
```

### `Progress.status()`

```py
Progress.status(status, *args, **kwargs)
```

记录运行任务的状态更新。

如果进度记录器是动画的，状态行将原地更新。

状态更新可按 `rate` 秒一次进行节流。

### `Progress.success()`

```py
Progress.success(status='Done', *args, **kwargs)
```

记录运行任务成功。不允许进一步状态更新。

如果 Logger 是动画的，动画会停止。

### `Progress.failure()`

```py
Progress.failure(message)
```

记录运行任务失败。不允许进一步状态更新。

如果 Logger 是动画的，动画会停止。

### `Progress.__weakref__`

对象的弱引用列表

## `class pwnlib.log.Logger`

```py
class pwnlib.log.Logger(logger: Logger | None = None)
```

类似于 `logging.LoggerAdapter` 的类。`logging.Logger` 实例上定义的所有公共方法都在此类上定义。

还添加了一些 `pwnlib` 风格：

- `progress()`（别名 `waitfor()`）
- `success()`
- `failure()`
- `indented()`
- `info_once()`
- `warning_once()`（别名 `warn_once()`）

通过日志记录的 `extra` 字段添加 `pwnlib` 特定的着色、缩进和进度日志信息。

使用 `getLogger()` 实例化的记录器将是此类的实例。

### `Logger.__init__(logger=None)`

```py
Logger.__init__(logger: Logger | None = None)
```

### `Logger.progress() -> Progress`

```py
Logger.progress(message, status='', *args, level=logging.INFO, **kwargs) -> Progress
```

创建一个新的进度记录器，生成日志级别为 `level` 的日志记录。

可以指定可选的 `rate` 参数来控制状态更新的频率。对 `Progress.status()` 的调用将节流为最多每 `rate` 秒更新一次。被节流的状态更新根本不会被发出，因此不会出现在日志文件中。使用此参数可避免在紧密循环中生成过多日志记录。

进度状态可以使用 `Progress.status()` 更新，并使用 `Progress.success()` 或 `Progress.failure()` 停止。

如果 `term.term_mode` 已启用，进度记录器将是动画的。

进度管理器也可用作上下文管理器。使用上下文管理器可确保即使抛出异常，动画也会停止。

```py
with log.progress('Trying something...') as p:
    for i in range(10):
        p.status("At %i" % i)
        time.sleep(0.5)
    x = 1/0
```

### `Logger.waitfor() -> Progress`

```py
Logger.waitfor(*args: Any, **kwargs: Any) -> Progress
```

`progress()` 的别名。

### `Logger.indented()`

```py
Logger.indented(message, *args, level=logging.INFO, **kwargs)
```

记录一条消息，但不在其前面放置行前缀。

- `level`（`int`）  
  用于设置缩进消息的备用日志级别。默认值为 `logging.INFO`。

### `Logger.success()`

```py
Logger.success(message, *args, **kwargs)
```

记录一条成功消息。

### `Logger.failure()`

```py
Logger.failure(message, *args, **kwargs)
```

记录一条失败消息。

### `Logger.info_once()`

```py
Logger.info_once(message, *args, **kwargs)
```

记录一条信息消息。同一条消息不会再次打印。

### `Logger.warning_once()`

```py
Logger.warning_once(message, *args, **kwargs)
```

记录一条警告消息。同一条消息不会再次打印。

### `Logger.warn_once() -> None`

```py
Logger.warn_once(*args: Any, **kwargs: Any) -> None
```

`warning_once()` 的别名。

### `Logger.debug()`

```py
Logger.debug(message, *args, **kwargs)
```

记录一条调试消息。

### `Logger.info()`

```py
Logger.info(message, *args, **kwargs)
```

记录一条信息消息。

### `Logger.maybe_hexdump()`

```py
Logger.maybe_hexdump(self, message, *args, **kwargs)
```

使用 `indented` 记录一条消息。重复的单个字节会被压缩，不可打印的消息会进行 hexdump。

### `Logger.warning()`

```py
Logger.warning(message, *args, **kwargs)
```

记录一条警告消息。

### `Logger.warn() -> None`

```py
Logger.warn(*args: Any, **kwargs: Any) -> None
```

`warning()` 的别名。

### `Logger.error()`

```py
Logger.error(message, *args, **kwargs)
```

在异常处理器外部调用。

记录一条错误消息，然后抛出 `PwnlibException`。

### `Logger.exception()`

```py
Logger.exception(message, *args, **kwargs)
```

从异常处理器中调用。

记录一条错误消息，然后重新抛出当前异常。

### `Logger.critical()`

```py
Logger.critical(message, *args, **kwargs)
```

记录一条严重消息。

### `Logger.log()`

```py
Logger.log(level, message, *args, **kwargs)
```

记录一条日志级别为 `level` 的消息。`pwnlib` 格式化器将使用默认的 `logging` 格式化器来格式化此消息。

### `Logger.isEnabledFor() -> bool`

```py
Logger.isEnabledFor(level) -> bool
```

查看底层记录器是否启用了指定级别。

### `Logger.setLevel()`

```py
Logger.setLevel(level)
```

设置底层记录器的日志级别。

### `Logger.addHandler()`

```py
Logger.addHandler(handler)
```

将指定处理器添加到���层记录器。

### `Logger.removeHandler()`

```py
Logger.removeHandler(handler)
```

从底层记录器移除指定处理器。

### `Logger.__weakref__`

对象的弱引用列表

## `class pwnlib.log.Handler`

```py
class pwnlib.log.Handler(stream=None)
```

自定义处理器类。此类将把当前设置的 `context.log_level` 报告为其日志级别。

如果 `term.term_mode` 已启用，则源自进度记录器的日志记录不会被发出，而是会创建动画进度行。

此处理器的一个实例会被添加到 `'pwnlib'` 记录器。

初始化处理器。

如果未指定 stream，则使用 `sys.stderr`。

### `Handler.emit()`

```py
Handler.emit(record)
```

根据 `term.term_mode` 是否启用，发出日志记录或创建/更新动画进度记录器。

## `class pwnlib.log.Formatter`

```py
class pwnlib.log.Formatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)
```

日志格式化器，对包含 `'pwnlib_msgtype'` 属性的日志记录执行自定义格式化。其他记录使用 `logging` 模块的默认格式化器格式化。

如果设置了 `'pwnlib_msgtype'`，它会执行以下操作：

- 在 `_msgtype_prefixes` 中查找前缀并添加到消息前。
- 为消息添加前缀，使其从第四列开始。
- 如果消息跨越多行，则进行拆分，所有后续行都缩进。

此格式化器由安装在 `'pwnlib'` 记录器上的处理器使用。

使用指定的格式字符串初始化格式化器。

使用指定格式字符串或上述默认值初始化格式化器。允许使用可选的 `datefmt` 参数进行专门日期格式化。如果省略 `datefmt`，则获得类似 ISO8601（或类似 RFC 3339）的格式。

使用样式参数 `'%'`、`'{'` 或 `'$'` 来指定在格式字符串中使用 %-格式化、`str.format()`（`{}`）格式化或 `string.Template` 格式化。

**版本变更：** 在 3.2 版本中变更：添加了 `style` 参数。

### `Formatter.format() -> str`

```py
Formatter.format(record: LogRecord) -> str
```

将指定记录格式化为文本。

记录的属性字典用作字符串格式化操作的操作数，该操作产生返回的字符串。在格式化字典之前，会执行几个准备步骤。记录的 message 属性使用 `LogRecord.getMessage()` 计算。如果格式化字符串使用时间（由调用 `usesTime()` 确定），则调用 `formatTime()` 格式化事件时间。如果有异常信息，则使用 `formatException()` 格式化并附加到消息中。