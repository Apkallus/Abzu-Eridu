# datetime --- 基本日期和时间类型

https://docs.python.org/zh-cn/3/library/datetime.html

`datetime` 模块提供了用于操作日期和时间的类。

## timedelta 对象

`timedelta` 对象表示一段持续的时间，即两个 `datetime` 或 `date` 实例之间的差值。

### class datetime.timedelta()

```py
class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
```

所有参数都是可选的并且默认为 0。 这些参数可以是整数或者浮点数，并可以为正值或者负值。

参数单位的换算规则如下：

- 1毫秒会转换成1000微秒
- 1分钟会转换成60秒
- 1小时会转换成3600秒
- 1星期会转换成7天

#### timedelta.total_seconds()

```py
timedelta.total_seconds()
```
返回时间区间包含的总秒数。

## time 对象

一个 `time` 对象代表某日的（本地）时间，它独立于任何特定日期，并可通过 `tzinfo` 对象来调整。

### class datetime.time()

```py
class datetime.time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
```

所有参数都是可选的。 `tzinfo` 可以是 `None`，或者是一个 `tzinfo` 子类的实例。 

#### classmethod time.fromisoformat()

```py
classmethod time.fromisoformat(time_string)
```

返回一个对应于以任何有效的 ISO 8601 格式给出的 `time_string` 的 `time`