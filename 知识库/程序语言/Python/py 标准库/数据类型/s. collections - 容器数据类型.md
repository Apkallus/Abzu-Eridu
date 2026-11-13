https://docs.python.org/zh-cn/3/library/collections.html

# collections --- 容器数据类型

这个模块实现了一些专门化的容器

- `deque`  
    类似列表的容器，但 `append` 和 `pop` 在其两端的速度都很快。


## namedtuple() 命名元组的工厂函数

命名元组赋予每个位置一个含义，提供可读性和自文档性。它们可以用于任何普通元组，并添加了通过名字获取值的能力，通过索引值也是可以的。

### collections.namedtuple()

```py
collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)
```

返回一个新的名为 `typename` 的元组子类。 这个新子类将被用于创建具有即可通过索引和迭代又可通过属性查找来访问的字段的元组型对象。 这样的子类实例还将具有文档字符串 (包含 `typename` 和 `field_names`) 和以 `name=value` 格式列出元组内容的 `__repr__()` 方法以方便使用。

`field_names` 是一个像 `['x', 'y']` 一样的字符串序列。另外 `field_names` 可以是一个纯字符串，用空白或逗号分隔开元素名，比如 `'x y'` 或者 `'x, y'` 。

## class collections.deque()

```py
class collections.deque([iterable[, maxlen]])
```

返回一个新的双向队列对象，从左到右初始化(用方法 `append()`) ，从 `iterable` 数据创建。如果 `iterable` 没有指定，新队列为空。

虽然 `list` 对象也支持类似的操作，但它们是针对快速的固定长度的操作进行优化而 `pop(0)` 和 `insert(0, v)` 操作对下层数据表示的大小和位置改变都将产生 `O(n)` 的内存移动开销。

如果 `maxlen` 没有指定或者是 `None` ，`deques` 可以增长到任意长度。否则，`deque`就限定到指定最大长度。一旦限定长度的`deque`满了，当新项加入时，同样数量的项就从另一端弹出。

`deque` 对象支持以下方法：

- `append(item, /)`  
    添加 `item` 到双端队列的右端。

- `appendleft(item, /)`  
    添加 `item` 到双端队列的左端。

- `pop()`  
    移去并且返回 deque 最右侧的一个元素。 若无则引发一个 `IndexError`

- `popleft()`  
    移去并且返回 deque 最左侧的一个元素。 若无则引发一个 `IndexError`


- `remove(value, /)`  
    移除找到的第一个 `value`。 如果没有的话就引发 `ValueError`。
