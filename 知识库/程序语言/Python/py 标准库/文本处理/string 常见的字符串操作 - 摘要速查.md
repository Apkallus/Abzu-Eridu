# string - 常见的字符串操作

https://docs.python.org/zh-cn/3/library/string.html

## 字符串常量

此模块中定义的常量为：

- `string.ascii_letters`  
    下文所述 `[ascii_lowercase]` 和 `[ascii_uppercase]` 常量的拼接。该值不依赖于语言区域。

- `string.ascii_lowercase`  
    小写字母 `'abcdefghijklmnopqrstuvwxyz'`。该值不依赖于语言区域，不会发生改变。

- `string.ascii_uppercase`  
    大写字母 `'ABCDEFGHIJKLMNOPQRSTUVWXYZ'`。该值不依赖于语言区域，不会发生改变。

- `string.digits`  
    字符串 `'0123456789'`。

- `string.hexdigits`  
    字符串 `'0123456789abcdefABCDEF'`。

- `string.punctuation`  
    由在 `C` 区域设置中被视为标点符号的 ASCII 字符所组成的字符串：``!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~``。

- `string.printable`  
    由被视为可打印符号的 ASCII 字符组成的字符串。这是 `[digits]`、`[ascii_letters]`、`[punctuation]` 和 `[whitespace]` 的总和。

- `string.whitespace`  
    由被视为空白符号的 ASCII 字符组成的字符串。其中包括空格、制表符、换行符、回车符、换页符和垂直制表符。

## 格式字符串语法

格式字符串包含有以花括号 `{}` 括起来的“替换字段”。不在花括号之内的内容被视为字面文本，会不加修改地复制到输出中。 在字面文本中包含花括号字符，通过重复来转义: `{{` 和 `}}`。


替换字段的语法如下：

replacement_field  
`"{" [field_name] ["!" conversion] [":" format_spec] "}"`

- field_name  
    `arg_name ("." attribute_name | "[" element_index "]")*`

    - arg_name  
        `[identifier | digit+]`
    - attribute_name  
        `identifier`
    - element_index  
        `digit+ | index_string`
        - index_string  
            `<any source character except "]">+`

- conversion  
    `"r" | "s" | "a"`

- format_spec  
    `format-spec:format_spec`


`conversion` 字段会在格式化之前进行类型强制转换。

```py
"Harold's a clever {0!s}"        # 先在参数上调用 str()
"Bring out the holy {name!r}"    # 先在参数上调用 repr()
"More {!a}"                      # 先在参数上调用 ascii()
```
> 其中 `!r` 打印字节串 `b''` 而在 ctf 中最常用

`format_spec` 字段包含值应如何呈现的规格描述，例如字段宽度、对齐、填充、小数精度等细节信息。每种值类型可以定义自己的“格式化迷你语言”或对 `format_spec` 的解读方式。大多数内置类型都支持同样的格式化迷你语言

例：
```py
# 以拥有 `0x` 前缀的十六进制打印数字
f"{int_number:#x}"

# 打印无 `0x`前缀的十六进制数字，使用0填充到8位
f"{num:08x}"
```

### 格式规格迷你语言

标准格式说明符 的一般形式如下：

format_spec  
`[options][width_and_precision][type]`

- options  
    `[[fill]align][sign]["z"]["#"]["0"]`
    - fill  
        `<any character>`
    - align  
        `"<" | ">" | "=" | "^"`
    - sign  
        `"+" | "-" | " "`

- width_and_precision  
    `[width_with_grouping][precision_with_grouping]`

    - width_with_grouping  
        `[width][grouping]`
        - width  
            `digit+`
        - grouping  
            `"," | "_"`

    - precision_with_grouping  
        `"." [precision][grouping] | "." grouping`
        - precision  
            `digit+`
        - grouping  
            `"," | "_"`

- type  
    `"b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"`

options
- `align` 对齐
    - 指定时可选设置填充字符 `fill`，省略时默认为空格
    - `"<" | ">" | "=" | "^"` 分别对应对齐格式：  
        左；右；符号与数字间；居中

- `sign` 数字的正负符号
    - `"+" | "-" | " "` 分别对应符号格式：  
        正负数；仅负数（默认）；正数前导空格，负数负号

- `#` 替代形式，仅适用于整数、浮点数和复数类型
    - 对于整数类型，当使用二进制、八进制或十六进制输出时，此选项会为输出值分别添加相应的 `'0b'`, `'0o'`, `'0x'` 或 `'0X'` 前缀。

width_and_precision
- `width` 十进制整数，定义最小字段宽度  
    当未显式给出对齐方式时，在 width 字符前加一个零 `'0'` 字符将为数字类型启用感知正负号的零填充

type 数据呈现

## 模板字符串（`$-strings`）

> **注意**
>
> 此处描述的功能引入于 Python 2.4，是一种基于正则表达式的简单模板方法。它早于 `[str.format()]`、[格式化字符串字面量] 以及 [模板字符串字面量]。它与 Python 3.14 中引入的模板字符串字面量（t-strings）无关。t-strings 的求值结果为 `[string.templatelib.Template]` 对象，位于 `[string.templatelib]` 模块中。

模板字符串提供了更简单的字符串替换功能，详见 [PEP 292]。

模板字符串支持基于 `$` 的替换，规则如下：

- `$$`  
    转义符；替换为单个 `$`。

- `$identifier`  
    命名替换占位符，匹配映射键 `"identifier"`。默认情况下，`"identifier"` 仅限于以 ASCII 字母或下划线开头的、不区分大小写的 ASCII 字母数字字符串（含下划线）。`$` 字符后的第一个非标识符字符即终止该占位符规范。

- `${identifier}`  
    等同于 `$identifier`。当占位符后紧跟有效标识符字符但该字符不属于占位符的一部分时（例如 `"${noun}ification"`），必须使用此形式。

- 其他 `$` 用法  
    字符串中任何其他形式的 `$` 出现都将导致引发 `[ValueError]`。


示例

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

### class string.Template() —— 构造器

```python
class string.Template(template)
```

该构造器接受一个参数作为模板字符串。

#### substitute() —— 完全替换

```python
substitute(mapping={}, /, **kwds)
```

执行模板替换并返回新字符串。`mapping` 可以是任何字典类对象，其键需与模板中的占位符匹配。或者，可以提供关键字参数，关键字即为占位符名称。当同时提供 `mapping` 和 `kwds` 且存在重复键时，`kwds` 中的占位符优先。

#### safe_substitute() —— 部分替换

```python
safe_substitute(mapping={}, /, **kwds)
```

与 `[substitute()]` 类似，但如果 `mapping` 和 `kwds` 中缺少占位符，不会引发 `[KeyError]` 异常，而是将原始占位符完整保留在结果字符串中。此外，与 `substitute()` 不同，任何其他 `$` 的出现只会返回 `$`，而不会引发 `[ValueError]`。

虽然仍可能发生其他异常，但该方法被称为“safe”（安全），因为它总是尝试返回可用的字符串而非抛出异常。
