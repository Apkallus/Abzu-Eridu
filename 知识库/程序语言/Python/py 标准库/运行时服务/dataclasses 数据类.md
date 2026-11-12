# dataclasses --- 数据类

https://docs.python.org/zh-cn/3/library/dataclasses.html

此模块提供了一个装饰器和一些函数，用于自动为用户自定义的类添加诸如 `__init__()` 和 `__repr__()` 等生成的[特殊方法]。它最初在 [PEP 557] 中被描述。

要在这些生成的方法中使用成员变量，需要使用 [PEP 526] 的类型注解进行定义。例如，以下代码：

```py
from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
```

将会添加一个类似于下面的 `__init__()` 方法，以及其他方法：

```py
def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
    self.name = name
    self.unit_price = unit_price
    self.quantity_on_hand = quantity_on_hand
```

## 模块内容

### @dataclasses.dataclass()

```py
@dataclasses.dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False)
```

该函数是一个 `decorator`（装饰器），用于向类中添加生成的 `special methods`（特殊方法），如下所述。

### dataclasses.field()

```py
dataclasses.field(*, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None, kw_only=MISSING, doc=None)
```

对于常见且简单的用例，不需要其他功能。但是，某些数据类特性需要每个字段的附加信息。为了满足对附加信息的需求，你可以用对提供的 `field()` 函数的调用来替换默认的字段值。例如

```py
@dataclass
class C:
    mylist: list[int] = field(default_factory=list)

c = C()
c.mylist += [1, 2, 3]
```

- `default_factory`  
    如果提供，它必须是一个零参数的可调用对象，当需要为该字段提供默认值时将调用它。除其他用途外，这可用于指定具有可变默认值的字段，如下文所述。

- `slots`  
    如为真值 (默认为 `False`)，则将生成 `__slots__` 属性并返回一个新类而非原本的类。 
    > 不创建属性的字典，直接使用列表索引。作为数据容器时日常添加（直到报错）