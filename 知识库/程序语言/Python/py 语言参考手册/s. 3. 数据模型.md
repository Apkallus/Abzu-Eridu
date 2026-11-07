# 3. Data model

https://docs.python.org/zh-cn/3/reference/datamodel.html

## 3.2. 标准类型层级结构

Python 内置类型

### 3.2.3. Ellipsis —— 省略

此类型只有一种取值。是一个具有此值的单独对象。此对象通过字面值 `...` 或内置名称 `Ellipsis` 访问。它的逻辑值为真。

### 3.2.8. 可调用类型

此类型可以被应用于函数调用操作

#### 3.2.8.1. 用户定义函数

用户定义函数对象可通过函数定义来创建

##### 3.2.8.1.1. 特殊的只读属性

```py
function.__builtins__
```
- 指向保存函数内置命名空间的 [字典] 的引用。

```py
function.__globals__
```
- 对存放该函数中 [全局变量] 的 [字典] 的引用 —— 函数定义所在模块的全局命名空间。

## 3.3. Special method names

### 3.3.1. Basic customization

[`object.__bool__(self)`](https://docs.python.org/3.14/reference/datamodel.html#object.__bool__)

调用以实现真值测试和内置操作 `bool()`；应返回 `False` 或 `True`。当未定义此方法时，如果定义了 [`__len__()`](#object.__len__)，则调用它，并且如果其结果非零，则认为对象为真。如果一个类既没有定义 `__len__()` 也没有定义 `__bool__()`（[`object`](../builtins/functions.html#object) 类本身就是这样），则其所有实例都被视为真。

> 即，当对象未定义布尔方法时，且定义数量方法时，返回结果取决于对象内的元素数量
> - 对于 XML tree，当标签存在且包含文本，但标签内无子标签，则返回 false

### 3.3.7. 模拟容器类型

#### `object.__getitem__()`

```py
object.__getitem__(self, subscript)
```

被调用以实现抽取条目，即 `self[subscript]`。用于内支对象：
- 序列
- 映射（键值对）