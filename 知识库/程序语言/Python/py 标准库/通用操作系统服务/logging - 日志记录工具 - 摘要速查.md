# logging - Python 的日志记录工具

https://docs.python.org/zh-cn/3/library/logging.html

### debug()

```py
debug(msg, *args, **kwargs)
```

在此记录器上记录 [DEBUG] 级别的消息。 `msg` 是消息格式字符串，而 `args` 是用于字符串格式化操作合并到 `msg` 的参数。（请注意，这意味着您可以在格式字符串中使用关键字以及单个字典参数。）当未提供 `args` 时，不会对 `msg` 执行 `%` 格式化操作。

### info()

```py
info(msg, *args, **kwargs)
```

在此记录器上记录 [INFO] 级别的消息。参数解释同 `debug()`。

### warning()

```py
warning(msg, *args, **kwargs)
```

在此记录器上记录 [WARNING] 级别的消息。参数解释同 `debug()`。