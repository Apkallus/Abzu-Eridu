https://docs.python.org/zh-cn/3/library/collections.abc.html

# collections.abc --- 容器的抽象基类

该模块曾是 `collections` 模块的组成部分。

本模块提供了一些 “抽象基类”，它们可被用于测试一个类是否提供某个特定的接口；例如，它是否为 `hashable` 或是否为 `mapping` 等。


## 容器抽象基类

### class collections.abc.Callable

```py
class collections.abc.Callable
```

用于提供 `__call__()` 方法的类的 ABC

### class collections.abc.Iterable
 
```py 
class collections.abc.Iterable
```

用于提供 `__iter__()` 方法的类的 ABC

> `dict.values()`

### class collections.abc.Sequence, class collections.abc.MutableSequence, class collections.abc.ByteString

```py
class collections.abc.Sequence
class collections.abc.MutableSequence
class collections.abc.ByteString
```

只读的与可变的 “序列” 的抽象基类。

> `list`

### class collections.abc.MappingView, class collections.abc.ItemsView, class collections.abc.KeysView, class collections.abc.ValuesView

```py
class collections.abc.MappingView
class collections.abc.ItemsView
class collections.abc.KeysView
class collections.abc.ValuesView
```

映射、条目、键和值的 “视图” 的抽象基类。