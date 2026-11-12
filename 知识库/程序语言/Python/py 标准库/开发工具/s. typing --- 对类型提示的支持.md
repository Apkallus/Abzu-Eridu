# typing --- 对类型提示的支持

https://docs.python.org/zh-cn/3/library/typing.html#module-typing

> 备注：Python 运行时不强制要求函数与变量类型标注。 它们可被 [类型检查器]、IDE、语法检查器等第三方工具使用。 

本模块提供了对类型提示的运行时支持。

## 标注可调用对象

函数或是其他 `callable` 对象，使用 `collections.abc.Callable` 或已被弃用的 `typing.Callable` 来标注。 `Callable[[int], str]` 表示一个接受 `int` 类型的单个形参并返回一个 `str` 的函数。

下标语法总是要刚好使用两个值：参数列表和返回类型。 参数列表必须是一个由类型组成的列表、`ParamSpec`、`Concatenate` 或省略号 `...`。 返回类型必须是单一类型。

如果将一个省略号字面值 `...` 作为参数列表，则表示可以接受包含任意形参列表的可调用对象

## 标注元组

对于 Python 中的大多数容器，类型系统会假定容器中的所有元素都是相同类型的。但 `tuple` 可以接受 任意数量 的类型参数

要表示一个可以是 任意 长度的元组，并且其中的所有元素都是相同类型的 `T`，请使用字面值省略号 `...`: `tuple[T, ...]`。要表示空元组，请使用 `tuple[()]`。只使用 `tuple` 作为注解等效于使用 `tuple[Any, ...]`


## 其他特殊指令

### class typing.NamedTuple

```py
class typing.NamedTuple
```

用法:

```py
class Employee(NamedTuple):
    name: str
    id: int
```

这相当于：

```py
Employee = collections.namedtuple('Employee', ['name', 'id'])
```