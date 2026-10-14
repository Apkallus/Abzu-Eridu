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

#####  class lxml.etree._ElementTree

Bases: `object`

###### parse()

```py
parse(self, source, parser=None, base_url=None)
```

Updates self with the content of source and returns its root.

> `parser` 即为 `lxml.etree.XMLParser`

##### 🖇️ class lxml.etree.XMLParser —— XML 解析器

https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser

```python
class lxml.etree.XMLParser(
    self,
    encoding=None,
    attribute_defaults=False,
    dtd_validation=False,
    load_dtd=False,
    no_network=True,
    decompress=False,
    ns_clean=False,
    recover=False,
    schema: [XMLSchema] = None,
    huge_tree=False,
    remove_blank_text=False,
    resolve_entities='internal',
    remove_comments=False,
    remove_pis=False,
    strip_cdata=True,
    collect_ids=True,
    target=None,
    compact=True
)
```

基类：`[_FeedParser]`

XML 解析器。

解析器可作为附加参数传递给 lxml API 的各种解析函数。系统始终提供一个默认解析器，可通过调用全局函数 `set_default_parser` 进行替换。新解析器可以随时创建，而不会产生显著的运行时开销。

构造函数中的关键字参数主要基于 libxml2 解析器的配置。如果请求了 DTD 验证或属性默认值，则还会加载 DTD（除非你额外提供了一个 [XMLSchema]，从中可以读取默认属性）。

可用的布尔型关键字参数：

- attribute_defaults
  从 DTD 或 XMLSchema 注入默认属性
- dtd_validation
  根据文档引用的 DTD 进行验证
- load_dtd 🎯
  使用 DTD 进行解析
- no_network
  阻止对相关文件的网络访问（默认值：True）
- decompress
  自动解压缩 gzip 输入（默认值：False，在 lxml 6.0 中变更，禁用仅影响 libxml2 2.15+）
- ns_clean
  清理冗余的命名空间声明
- recover
  尽力解析格式错误的 XML
- remove_blank_text
  丢弃看似可忽略的空白文本节点。在没有 DTD/Schema 的情况下，启发式算法会保留同一层级中出现在非空白内容之后的空白文本节点
- remove_comments
  丢弃注释
- remove_pis
  丢弃处理指令
- strip_cdata
  将 CDATA 部分替换为普通文本内容（默认值：True）
- compact
  为短文本内容节省内存（默认值：True）
- collect_ids
  使用 XML ID 哈希表以实现快速访问（默认值：True，在 DTD 验证时始终为 True）
- huge_tree
  禁用安全限制，支持非常深的树结构和非常长的文本内容

其他关键字参数：

- resolve_entities 🎯
  将实体替换为其文本值。设为 False 保留实体引用，设为 True 解析所有实体，设为 `internal` 仅解析内部定义（不访问外部文件/URL）。默认值曾为 True，在 lxml 5.0 中更改为 `internal`
- encoding
  覆盖文档编码（注意：使用 libiconv 编码名称）
- target
  一个解析器目标对象，用于接收解析事件
- schema
  用于验证的 [XMLSchema]

请注意，应避免在线程之间共享解析器。虽然这不会造成危害，但使用独立的解析器效率更高。此限制不适用于默认解析器。

### api —— APIs specific to lxml.etree

#### iteration

https://lxml.de/api.html#iteration

The ElementTree API makes Elements iterable to support iteration over their children. Using the tree defined above, we get:

```py
>>> [ child.tag for child in root ]
['a', 'b', 'c', 'd']
```
