https://docs.python.org/zh-cn/3.14/library/string.html

# string - 常见的字符串操作

## 字符串常量

此模块中定义的常量为：

-   `string.ascii_letters`
    下文所述 `[ascii_lowercase]` 和 `[ascii_uppercase]` 常量的拼接。该值不依赖于语言区域。

-   `string.ascii_lowercase`
    小写字母 `'abcdefghijklmnopqrstuvwxyz'`。该值不依赖于语言区域，不会发生改变。

-   `string.ascii_uppercase`
    大写字母 `'ABCDEFGHIJKLMNOPQRSTUVWXYZ'`。该值不依赖于语言区域，不会发生改变。

-   `string.digits`
    字符串 `'0123456789'`。

-   `string.hexdigits`
    字符串 `'0123456789abcdefABCDEF'`。

-   `string.octdigits`
    字符串 `'01234567'`。

-   `string.punctuation`
    由在 `C` 区域设置中被视为标点符号的 ASCII 字符所组成的字符串：``!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~``。

-   `string.printable`
    由被视为可打印符号的 ASCII 字符组成的字符串。这是 `[digits]`、`[ascii_letters]`、`[punctuation]` 和 `[whitespace]` 的总和。

    > **备注**
    > 根据设计，`str.isprintable()` 对 `[string.printable]` 中的某些字符将返回 `False`。特别地，`string.printable` 在 POSIX 中并非全部可打印（参见 LC_CTYPE）。

-   `string.whitespace`
    由被视为空白符号的 ASCII 字符组成的字符串。其中包括空格、制表符、换行符、回车符、换页符和垂直制表符。

## 模板字符串（`$-strings`）

https://docs.python.org/zh-cn/3.14/library/string.html#template-strings-strings

> **注意**
>
> 此处描述的功能引入于 Python 2.4，是一种基于正则表达式的简单模板方法。它早于 `[str.format()]`、[格式化字符串字面量] 以及 [模板字符串字面量]。它与 Python 3.14 中引入的模板字符串字面量（t-strings）无关。t-strings 的求值结果为 `[string.templatelib.Template]` 对象，位于 `[string.templatelib]` 模块中。

模板字符串提供了更简单的字符串替换功能，详见 [PEP 292]。模板字符串的主要用例是国际化（i18n），因为在该场景下，其简洁的语法和功能使得翻译工作比使用 Python 其他内置字符串格式化设施更为容易。有关基于模板字符串构建的 i18n 库示例，请参阅 [flufl.i18n] 包。

模板字符串支持基于 `$` 的替换，规则如下：

-   `$$`
    转义符；替换为单个 `$`。
-   `$identifier`
    命名替换占位符，匹配映射键 `"identifier"`。默认情况下，`"identifier"` 仅限于以 ASCII 字母或下划线开头的、不区分大小写的 ASCII 字母数字字符串（含下划线）。`$` 字符后的第一个非标识符字符即终止该占位符规范。
-   `${identifier}`
    等同于 `$identifier`。当占位符后紧跟有效标识符字符但该字符不属于占位符的一部分时（例如 `"${noun}ification"`），必须使用此形式。
-   其他 `$` 用法
    字符串中任何其他形式的 `$` 出现都将导致引发 `[ValueError]`。


```py
from string import Template

# 设置模板字符串
template = Template('Host: ${target_host}')
# 填充模板字符串
print(template.substitute(target_host="localhost"))


# 分段填充
foo = Template("${a} ${b}")

## 第一段
foo_a = foo.safe_substitute(a="1")
print(foo_a)
# 1 ${b}

## 第二段
foo_b = Template(foo_a).safe_substitute(b="2")
print(foo_b)
# 1 2
```


`string` 模块提供了实现上述规则的 `[Template]` 类。`Template` 的方法如下：

### class string.Template

```python
class string.Template(template)
```

-   构造函数
    接受单个参数作为模板字符串。

#### substitute()

```python
substitute(mapping={}, /, **kwds)
```

执行模板替换并返回新字符串。`mapping` 可以是任何字典类对象，其键需与模板中的占位符匹配。或者，可以提供关键字参数，关键字即为占位符名称。当同时提供 `mapping` 和 `kwds` 且存在重复键时，`kwds` 中的占位符优先。

#### safe_substitute()

```python
safe_substitute(mapping={}, /, **kwds)
```

与 [`substitute()`] 类似，但如果 `mapping` 和 `kwds` 中缺少占位符，不会引发 `[KeyError]` 异常，而是将原始占位符完整保留在结果字符串中。此外，与 `substitute()` 不同，任何其他 `$` 的出现只会返回 `$`，而不会引发 `[ValueError]`。

虽然仍可能发生其他异常，但该方法被称为“safe”（安全），因为它总是尝试返回可用的字符串而非抛出异常。从另一种意义上说，`safe_substitute()` 可能并不安全，因为它会静默忽略包含悬空分隔符、未匹配大括号或无效 Python 标识符占位符的格式错误模板。

#### is_valid()

```python
is_valid()
```

如果模板包含会导致 [`substitute()`] 引发 `[ValueError]` 的无效占位符，则返回 `False`。

3.11 版新增。

#### get_identifiers()

```python
get_identifiers()
```

按首次出现的顺序返回模板中有效标识符的列表，忽略任何无效标识符。

3.11 版新增。

`Template` 实例还提供一个公共数据属性：

#### template

这是传递给构造函数的 `template` 参数的对象。通常不应修改它，但未强制只读访问。

