# `pwnlib.log` — 日志功能

https://docs.pwntools.com/en/latest/log.html

用于在漏洞利用过程中打印状态以及在 `pwntools` 内部使用的日志记录模块。

## 漏洞利用开发者

通过使用标准的 `from pwn import *`，一个名为 `log` 的对象将被插入到全局命名空间中。你可以使用它在漏洞利用过程中打印状态消息。

例如：

```python
log.info('Hello, world!')
```

打印：

```text
[*] Hello, world!
```

此外，还有一些便捷机制可用于对正在运行的任务执行状态更新（例如在暴力破解时）：

```python
p = log.progress('Working')
p.status('Reticulating splines')
time.sleep(1)
p.success('Got a shell!')
```

日志的详细程度最容易通过设置全局 `context` 对象上的 `log_level` 来控制：

```python
log.info("No you see me")
context.log_level = 'error'
log.info("Now you don't")
```

此属性的目的是控制打印到屏幕上的内容，而不是控制实际发出的内容。这意味着你可以将所有日志事件放入日志文件，而只想在屏幕上看到其中一小部分。

## Pwnlib 开发者

可以通过以下方式将模块特定的日志记录器导入模块：

```python
from pwnlib.log import getLogger
log = getLogger(__name__)
```

这提供了一种简单的方法，可以通过编程方式或通过配置文件进行过滤以进行调试。

使用 `progress` 时，应使用 `with` 关键字来管理作用域，以确保在抛出异常时旋转指示器停止。

## 技术细节

假定你熟悉 [logging](https://docs.python.org/3/library/logging.html#module-logging) 模块。

创建一个名为 `pwnlib` 的 pwnlib 根日志记录器，并为其安装自定义处理器和格式化器。处理器从 `context.log_level` 确定其日志级别。

理想情况下，`context.log_level` 应只影响处理器将发出哪些记录，从而例如记录到文件时不会受其影响。但出于性能原因，在正常情况下记录所有内容是不可行的。特别是 `[pwnlib.tubes.tube]` 内部存在紧密循环，我们希望能够在调试时调试它们，但如果不进行调试，它们不应输出消息（即使输出到日志文件也不行）。因此，pwnlib 内部有一些地方，在 `context.log_level` 未设置为 `logging.DEBUG` 或更低时，甚至不会发出记录。

由 `Progress` 和 `Logger` 对象创建的日志记录会在 `extra` 字段上设置 `'pwnlib_msgtype'`，以指示生成了何种类型的消息。格式化器使用此信息在消息前添加符号，例如 `'[+] got a shell!'` 中的 `'[+] '`。

使用 `logging` 模块的标准格式化器时，此字段会被忽略。

进度日志记录器上的所有状态更新（因节流而未丢弃的）都会导致创建一条日志记录。然后 `extra` 字段会携带对 `Progress` 日志记录器的引用作为 `'pwnlib_progress'`。

如果自定义处理器确定 `term.term_mode` 已启用，则其 `extra` 字段中包含 `'pwnlib_progess'` 的日志记录将不会导致发出消息，而是会创建一个动画进度行（带旋转指示器！）。请注意，其他处理器仍将看到有意义的日志记录。

自定义处理器仅处理级别至少为 `context.log_level` 的日志记录。因此，例如如果将 `'pwnlib.tubes.ssh'` 的级别设置为 `'DEBUG'`，除非 `context.log_level` 也设置为 `'DEBUG'`，否则不会显示额外输出。但是，其他处理器将看到 `'pwnlib.tubes.ssh'` 日志记录器生成的额外日志记录。

---

### `install_default_handler()`

实例化一个 `[Handler]` 和 `[Formatter]`，并将它们安装到 `pwnlib` 根日志记录器。从导入 `[pwn]` 时会自动调用此函数。

---

### `class Progress()`

```py
class pwnlib.log.Progress(logger: Logger, msg: str, status: str, level: int, args: tuple[Any], kwargs: dict[str, Any])
```

用于生成与某个正在运行的任务相关联的日志记录的进度日志记录器。实例可用作上下文管理器，在退出时自动将正在运行的任务声明为成功，或在抛出异常时声明为失败。调用 `[success()]` 或 `[failure()]` 后，状态将无法再更新。

此类仅供内部使用。应使用 `[Logger.progress()]` 创建进度日志记录器。

#### `__init__()`

```py
__init__(logger: Logger, msg: str, status: str, level: int, args: tuple[Any], kwargs: dict[str, Any]) → None
```

#### `status()`

```py
status(status, *args, **kwargs)
```

记录正在运行任务的状态更新。

如果进度日志记录器是动画的，状态行将就地更新。

状态更新可按每 `rate` 秒一次进行节流。

#### `success()`

```py
success(status='Done', *args, **kwargs)
```

记录正在运行的任务已成功。不允许进一步的状态更新。

如果日志记录器是动画的，动画将停止。

#### `failure()`

```py
failure(message)
```

记录正在运行的任务已失败。不允许进一步的状态更新。

如果日志记录器是动画的，动画将停止。

#### `__weakref__`

对象的弱引用列表。

---

### `class Logger()`

```py
class pwnlib.log.Logger(logger: Logger | None = None)
```

类似于 [logging.LoggerAdapter](https://docs.python.org/3/library/logging.html#logging.LoggerAdapter) 的类。[logging.Logger](https://docs.python.org/3/library/logging.html#logging.Logger) 实例上定义的所有公共方法都在此类上定义。

还添加了一些 `pwnlib` 特色：

- `[progress()]`（别名 `[waitfor()]`）
- `[success()]`
- `[failure()]`
- `[indented()]`
- `[info_once()]`
- `[warning_once()]`（别名 `[warn_once()]`）

通过日志记录的 `extra` 字段添加 `pwnlib` 特定的着色、缩进和进度日志信息。

使用 `getLogger()` 实例化的日志记录器将是此类的实例。

#### `__init__()`

```py
__init__(logger: Logger | None = None)
```

#### `progress()`

```py
progress(message, status='', *args, level=logging.INFO, **kwargs) → Progress
```

创建一个新的进度日志记录器，以日志级别 `level` 创建日志记录。

可以指定可选的 `rate` 参数来控制状态更新的频率。对 `[Progress.status()]` 的调用将被节流为每 `rate` 秒最多一次更新。被节流的状态更新将完全不会发出，因此不会显示在日志文件中。使用此参数可避免在紧密循环中生成过多日志记录。

进度状态可以使用 `[Progress.status()]` 更新，并使用 `[Progress.success()]` 或 `[Progress.failure()]` 停止。

如果启用了 `term.term_mode`，进度日志记录器将进行动画显示。

进度管理器还可作为上下文管理器使用。使用上下文管理器可确保即使引发异常，动画也会停止。

```python
with log.progress('Trying something...') as p:
    for i in range(10):
        p.status("At %i" % i)
        time.sleep(0.5)
    x = 1/0
```

#### `waitfor()`

```py
waitfor(*args: Any, **kwargs: Any) → Progress
```

`[progress()]` 的别名。

#### `indented()`

```py
indented(message, *args, level=logging.INFO, **kwargs)
```

记录一条消息，但不添加行前缀。

**参数：**

- **level**（`int`）— 设置缩进消息的备用日志级别。默认为 `logging.INFO`。

#### `success()`

```py
success(message, *args, **kwargs)
```

记录一条成功消息。

#### `failure()`

```py
failure(message, *args, **kwargs)
```

记录一条失败消息。

#### `info_once()`

```py
info_once(message, *args, **kwargs)
```

记录一条信息消息。同一条消息永远不会再次打印。

#### `warning_once()`

```py
warning_once(message, *args, **kwargs)
```

记录一条警告消息。同一条消息永远不会再次打印。

#### `warn_once()`

```py
warn_once(*args: Any, **kwargs: Any) → None
```

`[warning_once()]` 的别名。

#### `debug()`

```py
debug(message, *args, **kwargs)
```

记录一条调试消息。

#### `info()`

```py
info(message, *args, **kwargs)
```

记录一条信息消息。

#### `maybe_hexdump()`

```py
maybe_hexdump(self, message, *args, **kwargs)
```

使用 `indented` 记录一条消息。重复的单字节会被压缩，不可打印的消息会进行十六进制转储。

#### `warning()`

```py
warning(message, *args, **kwargs)
```

记录一条警告消息。

#### `warn()`

```py
warn(*args: Any, **kwargs: Any) → None
```

`[warning()]` 的别名。

#### `error()`

```py
error(message, *args, **kwargs)
```

在异常处理器外部调用。

记录一条错误消息，然后引发 `PwnlibException`。

#### `exception()`

```py
exception(message, *args, **kwargs)
```

从异常处理器中调用。

记录一条错误消息，然后重新引发当前异常。

#### `critical()`

```py
critical(message, *args, **kwargs)
```

记录一条严重消息。

#### `log()`

```py
log(level, message, *args, **kwargs)
```

记录一条日志级别为 `level` 的消息。`pwnlib` 格式化器将使用默认的 [logging](https://docs.python.org/3/library/logging.html#module-logging) 格式化器来格式化此消息。

#### `isEnabledFor()`

```py
isEnabledFor(level) → bool
```

检查底层日志记录器是否启用了指定级别。

#### `setLevel()`

```py
setLevel(level)
```

设置底层日志记录器的日志记录级别。

#### `addHandler()`

```py
addHandler(handler)
```

将指定处理器添加到基础日志记录器。

#### `removeHandler()`

```py
removeHandler(handler)
```

从基础日志记录器中移除指定处理器。

#### `__weakref__`

对象的弱引用列表。

---

### `class Handler()`

```py
class pwnlib.log.Handler(stream=None)
```

自定义处理器类。此类将报告当前设置的 `context.log_level` 作为其日志级别。

如果启用了 `term.term_mode`，则来自进度日志记录器的日志记录将不会发出，而是会创建一个动画进度行。

此处理器的一个实例被添加到 `'pwnlib'` 日志记录器。

初始化处理器。

如果未指定 stream，则使用 `sys.stderr`。

#### `emit()`

```py
emit(record)
```

根据是否启用了 `term.term_mode`，发出日志记录或创建/更新动画进度日志记录器。

---

### `class Formatter()`

```py
class pwnlib.log.Formatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)
```

日志格式化器，对包含 `'pwnlib_msgtype'` 属性的日志记录执行自定义格式化。其他记录使用 `logging` 模块的默认格式化器进行格式化。

如果设置了 `'pwnlib_msgtype'`，它将执行以下操作：

- 在 `_msgtype_prefixes` 中查找的前缀会被添加到消息前面。
- 消息被添加前缀，使其从第四列开始。
- 如果消息跨越多行，它们会被拆分，所有后续行都会被缩进。

此格式化器由安装在 `'pwnlib'` 日志记录器上的处理器使用。

使用指定的格式字符串初始化格式化器。

使用指定的格式字符串或上述默认值初始化格式化器。允许使用可选的 `datefmt` 参数进行专门的日期格式化。如果省略 `datefmt`，则获得类似 ISO8601（或类似 RFC 3339）的格式。

使用 `'%'`、`'{'` 或 `'$'` 的 `style` 参数来指定你希望在格式字符串中使用 %-格式化、[str.format()](https://docs.python.org/3/builtins/stdtypes.html#str.format)（`{}`）格式化还是 [string.Template](https://docs.python.org/3/library/string.html#string.Template) 格式化。

> 在 3.2 版本中更改：添加了 `style` 参数。

#### `format()`

```py
format(record: LogRecord) → str
```

将指定记录格式化为文本。

记录的属性字典用作字符串格式化操作的操作数，该操作产生返回的字符串。在格式化字典之前，会执行几个准备步骤。记录的消息属性使用 `LogRecord.getMessage()` 计算。如果格式化字符串使用时间（由对 `usesTime()` 的调用确定），则调用 `formatTime()` 来格式化事件时间。如果有异常信息，则使用 `formatException()` 进行格式化并追加到消息中。