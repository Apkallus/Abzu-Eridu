https://lxml.de/

## Developing with lxml

### The lxml.etree Tutorial

https://lxml.de/tutorial.html

#### fromstring() 函数

`fromstring()` 函数是解析字符串最简单的方法：

```python
>>> some_xml_data = "<root>data</root>"

>>> root = etree.fromstring(some_xml_data)
>>> print(root.tag)
root
>>> etree.tostring(root)
b'<root>data</root>'
```

#### ElementPath

ElementTree 库自带一种简单的类 XPath 路径语言，称为 [ElementPath](https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support)。主要区别在于你可以在 ElementPath 表达式中使用 `{namespace}tag` 表示法。但是，值比较和函数等高级功能不可用。

ElementPath 最初由 Fredrik Lundh [实现](https://web.archive.org/web/20070920063445/http://www.effbot.org/zone/element-xpath.htm)。

除了[完整的 XPath 实现](xpathxslt.html#xpath)外，`lxml.etree` 还以与 ElementTree 相同的方式支持 ElementPath 语言，甚至使用（几乎）相同的实现。API 在此提供了四个方法，你可以在 Element 和 ElementTree 上找到它们：

- `iterfind()` 遍历所有匹配路径表达式的 Element
- `findall()` 返回匹配 Element 的列表
- `find()` 高效地只返回第一个匹配项
- `findtext()` 返回第一个匹配项的 `.text` 内容

以下是一些示例：

```python
>>> root = etree.XML("<root><a x='123'>aText<b/><c/><b/></a></root>")
```

查找 Element 的子元素：

```python
>>> print(root.find("b"))
None
>>> print(root.find("a").tag)
a
```

在树中的任意位置查找 Element：

```python
>>> print(root.find(".//b").tag)
b
>>> [ b.tag for b in root.iterfind(".//b") ]
['b', 'b']
```

查找具有特定属性的 Element：

```python
>>> print(root.findall(".//a[@x]")[0].tag)
a
>>> print(root.findall(".//a[@y]"))
[]
```

在 lxml 3.4 中，有一个新的辅助函数可以为 Element 生成结构化的 ElementPath 表达式：

```python
>>> tree = etree.ElementTree(root)
>>> a = root[0]
>>> print(tree.getelementpath(a[0]))
a/b[1]
>>> print(tree.getelementpath(a[1]))
a/c
>>> print(tree.getelementpath(a[2]))
a/b[2]
>>> tree.find(tree.getelementpath(a[2])) == a[2]
True
```

只要树未被修改，此路径表达式就代表给定元素的标识符，可用于之后在同一棵树中通过 `find()` 找到它。与 XPath 相比，ElementPath 表达式的优势在于，即使对于使用命名空间的文档，它们也是自包含的。

`.iter()` 方法是一个特殊情况，它仅按名称查找树中的特定标签，而不基于路径。这意味着以下命令在成功情况下是等价的：

```python
>>> print(root.find(".//b").tag)
b
>>> print(next(root.iterfind(".//b")).tag)
b
>>> print(next(root.iter("b")).tag)
b
```

请注意，如果没有找到匹配项，`.find()` 方法只返回 None，而另外两个示例会引发 `StopIteration` 异常。

> 注意，find 查找的是目标元素内是否包含元素，而非目标元素是否存在
> 当前目标元素不包含子元素是返回 false
> [开发者邮件](https://mail.python.org/archives/list/lxml@python.org/message/AYIAJ7RX75OIZ63ZHKNYH4NOYL5L4OHN/)

### apidoc

#### lxml.etree module

https://lxml.de/apidoc/lxml.etree.html


##### lxml.etree.ElementBase —— Element 基类

```py
class lxml.etree.ElementBase(*children, attrib=None, nsmap=None, **_extra)
```

Bases: `_Element`

The public Element class. 

对象
- `find(self, path, namespaces=None)`
    查找第一个匹配的子元素, by tag name or path.

- `getchildren(self)`
    返回所有直接子节点，按照文档顺序
    - 新版被废弃，说明中建议使用 `list(element)` 或迭代（模糊表述：普通迭代返回直接子节点）

- `tag`
    元素标签

-  `text`
    第一个子元素前的文本（文本不属于子元素）. This is either a string or the value None, if there was no text.

### api —— APIs specific to lxml.etree

#### iteration

https://lxml.de/api.html#iteration

The ElementTree API makes Elements iterable to support iteration over their children. Using the tree defined above, we get:

```py
>>> [ child.tag for child in root ]
['a', 'b', 'c', 'd']
```
