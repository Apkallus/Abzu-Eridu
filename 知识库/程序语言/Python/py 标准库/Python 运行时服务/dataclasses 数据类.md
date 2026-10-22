# dataclasses --- 数据类

https://docs.pythonlang.cn/3/library/dataclasses.html

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