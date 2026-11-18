https://peps.python.org/pep-0008/

# PEP 8 – Python 代码风格指南

| 项目 | 内容 |
|---|---|
| PEP | 8 |
| 标题 | Python 代码风格指南 |
| 作者 | Guido van Rossum <guido@python.org>、Barry Warsaw <barry@python.org>、Alyssa Coghlan <ncoghlan@gmail.com> |
| 状态 | 活跃 |
| 类型 | 流程 |
| 创建日期 | 2001-07-05 |
| 历史邮件 | 2001-07-05、2013-08-01 |

## 引言

本文档给出 Python 主发行版标准库中 Python 代码的编码约定。关于 Python C 实现中 C 代码的风格指南，请参阅配套的信息性 PEP：[PEP 7](https://peps.python.org/pep-0007/)。

本文档与 [PEP 257](https://peps.python.org/pep-0257/)（文档字符串约定）改编自 Guido 最初的 Python 风格指南文章，并加入了 Barry 风格指南中的一些内容 [^2]。

随着新约定的确立，以及旧约定因语言本身的变化而过时，本风格指南会随时间演进。

许多项目有自己的编码风格指南。如果发生冲突，对于该项目而言，项目特定指南优先。

## 愚蠢的一致性是小智者的心魔

Guido 的关键洞见之一是：代码被阅读的次数远多于被编写的次数。这里给出的指南旨在提高代码可读性，并使广泛的 Python 代码保持一致。正如 [PEP 20](https://peps.python.org/pep-0020/) 所说：“可读性很重要。”

风格指南关乎一致性。与本文档保持一致很重要。项目内部一致更重要。一个模块或函数内部一致最重要。

然而，要知道何时可以不保持一致——有时风格指南的建议并不适用。拿不准时，请运用最佳判断。看看其他示例，决定哪种看起来最好。并且不要犹豫，去提问！

特别要注意：不要仅仅为了遵守本 PEP 而破坏向后兼容性！

忽略某条指南的其他一些合理理由包括：

1. 应用该指南会让代码更难读，即使对于习惯阅读遵循本 PEP 代码的人也是如此。
2. 为了与同样违反该指南的周边代码保持一致（也许出于历史原因）——不过这也是清理他人遗留问题的机会（真正的 XP 风格）。
3. 因为相关代码早于该指南出现，且没有其他理由修改该代码。
4. 因为代码需要与不支持风格指南所推荐特性的旧版 Python 保持兼容。

## 代码布局

### 缩进

每个缩进层级使用 4 个空格。

续行应使用 Python 在圆括号、方括号和花括号内的隐式行连接，将包裹元素垂直对齐，或使用*悬挂缩进*[^fn-hi]。使用悬挂缩进时，应考虑以下事项：第一行不应有参数，并且应使用进一步缩进以清楚表明这是续行：

**正确：**

```python
# 与开定界符对齐。
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# 增加 4 个空格（额外一级缩进），以区分参数与其他内容。
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# 悬挂缩进应增加一级。
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

**错误：**

```python
# 不使用垂直对齐时，禁止在第一行放置参数。
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# 缩进无法区分时，需要进一步缩进。
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

4 空格规则对续行是可选的。

可选：

```python
# 悬挂缩进*可以*缩进为 4 个空格以外的数量。
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```

当 `if` 语句的条件部分长到需要写成多行时，值得注意的是：两个字符的关键字 `if`、一个空格和一个左圆括号组合起来，会为多行条件的后续行自然形成 4 空格缩进。这可能会与 `if` 语句内部嵌套代码套件的缩进产生视觉冲突，因为后者也自然会缩进到 4 个空格。对于如何（或是否）进一步在视觉上区分这类条件行与 `if` 语句内部的嵌套套件，本 PEP 不明确表态。此情形下可接受的选项包括但不限于：

```python
# 不增加额外缩进。
if (this_is_one_thing and
    that_is_another_thing):
    do_something()

# 添加注释，在支持语法高亮的编辑器中提供一定区分。
if (this_is_one_thing and
    that_is_another_thing):
    # 由于两个条件都为真，我们可以 frobnicate。
    do_something()

# 在条件续行上增加一些额外缩进。
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

（另请参阅下文关于二元运算符之前还是之后换行的讨论。）

多行结构中的右花括号/方括号/圆括号可以对齐到列表最后一行的第一个非空白字符之下，例如：

```python
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```

也可以对齐到启动多行结构的那一行的第一个字符之下，例如：

```python
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

### 制表符还是空格？

空格是首选的缩进方法。

只有在需要与已经使用制表符缩进的代码保持一致时，才应使用制表符。

Python 不允许在缩进中混用制表符和空格。

### 最大行长度

将所有行限制为最多 79 个字符。

对于结构限制较少的长文本块（文档字符串或注释），行长度应限制为 72 个字符。

限制所需的编辑器窗口宽度，可以让多个文件并排打开，并且在使用以相邻列呈现两个版本的代码审查工具时效果很好。

大多数工具的默认换行会破坏代码的视觉结构，使其更难理解。选择这些限制是为了避免在窗口宽度设置为 80 的编辑器中发生换行，即使工具在换行时会在最后一列放置标记符号。某些基于 Web 的工具可能根本不提供动态换行。

有些团队强烈偏好更长的行长度。对于完全或主要由能够就此达成一致的团队维护的代码，可以将行长度限制提高到最多 99 个字符，前提是注释和文档字符串仍按 72 个字符换行。

Python 标准库较为保守，要求将行限制为 79 个字符（文档字符串/注释限制为 72 个字符）。

换行长行的首选方式是在圆括号、方括号和花括号内使用 Python 的隐式行续接。可以通过将表达式包裹在圆括号中，把长行拆成多行。应优先使用这种方式，而不是使用反斜杠进行行续接。

反斜杠有时仍然合适。例如，在 Python 3.10 之前，长的多个 `with` 语句无法使用隐式续接，因此这种情况下反斜杠是可以接受的：

```python
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

（关于这类多行 `with` 语句缩进的进一步思考，请参阅前面关于多行 `if` 语句的讨论。）

另一种这样的情况是 `assert` 语句。

确保适当缩进续行。

### 应在二元运算符之前还是之后换行？

几十年来，推荐风格一直是在二元运算符之后换行。但这会在两个方面损害可读性：运算符往往散布在屏幕上的不同列中，而且每个运算符都被移离其操作数，放到上一行。在这里，眼睛需要额外努力来判断哪些项是相加、哪些是相减：

**错误：**

```python
# 运算符与其操作数相距很远
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```

为了解决这个可读性问题，数学家和出版商遵循相反的惯例。Donald Knuth 在其 *Computers and Typesetting* 系列中解释了传统规则：“尽管段落中的公式总是在二元运算和关系之后换行，但展示公式总是在二元运算之前换行” [^3]。

遵循数学传统通常会产生更可读的代码：

**正确：**

```python
# 易于将运算符与操作数匹配
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

在 Python 代码中，允许在二元运算符之前或之后换行，只要该惯例在局部保持一致即可。对于新代码，建议采用 Knuth 风格。

### 空行

用两个空行包围顶层函数和类定义。

类内部的方法定义用一个空行包围。

可以（少量地）使用额外空行来分隔一组相关函数。在一组相关的一行式实现之间（例如一组占位实现），可以省略空行。

在函数内少量使用空行来表示逻辑区段。

Python 接受控制字符 L（即 `^L`）换页符作为空白；许多工具将其视为分页符，因此你可以用它们分隔文件中相关章节的页面。注意，某些编辑器和基于 Web 的代码查看器可能不将控制字符 L 识别为换页符，而会显示为其他字形。

### 源文件编码

核心 Python 发行版中的代码应始终使用 UTF-8，并且不应有编码声明。

在标准库中，非 UTF-8 编码只应用于测试目的。少用非 ASCII 字符，最好仅用于表示地名和人名。如果使用非 ASCII 字符作为数据，请避免嘈杂的 Unicode 字符，例如 `z̯̯͡a̧͎̺l̡͓̫g̹̲o̡̼̘` 和字节顺序标记。

Python 标准库中的所有标识符必须仅使用 ASCII 标识符，并且应尽可能使用英文单词（许多情况下会使用并非英文的缩写和技术术语）。

鼓励面向全球受众的开源项目采用类似策略。

### 导入

- 导入通常应各自单独成行：

  **正确：**

  ```python
  import os
  import sys
  ```

  **错误：**

  ```python
  import sys, os
  ```

  不过，下面这样是可以的：

  **正确：**

  ```python
  from subprocess import Popen, PIPE
  ```

- 导入总是放在文件顶部，位于任何模块注释和文档字符串之后，并在模块全局变量和常量之前。

  导入应按以下顺序分组：

  1. 标准库导入。
  2. 相关第三方导入。
  3. 本地应用/库特定导入。

  每组导入之间应放一个空行。

- 推荐使用绝对导入，因为它们通常更可读，并且当导入系统配置错误时（例如包内某个目录最终出现在 `sys.path` 上），通常表现更好（或至少给出更好的错误消息）：

  **正确：**

  ```python
  import mypkg.sibling
  from mypkg import sibling
  from mypkg.sibling import example
  ```

  然而，显式相对导入是绝对导入的可接受替代方案，尤其是在处理复杂包布局时，因为使用绝对导入会不必要地冗长：

  **正确：**

  ```python
  from . import sibling
  from .sibling import example
  ```

  标准库代码应避免复杂包布局，并始终使用绝对导入。

- 当从包含类的模块中导入类时，通常可以这样写：

  **正确：**

  ```python
  from myclass import MyClass
  from foo.bar.yourclass import YourClass
  ```

  如果这种写法导致本地名称冲突，则显式写出：

  **正确：**

  ```python
  import myclass
  import foo.bar.yourclass
  ```

  并使用 `myclass.MyClass` 和 `foo.bar.yourclass.YourClass`。

- 应避免通配符导入（`from <module> import *`），因为它们使命名空间中存在哪些名称变得不清楚，既会混淆读者，也会混淆许多自动化工具。通配符导入有一种可辩护的用例：将内部接口作为公共 API 的一部分重新发布（例如，用可选加速模块中的定义覆盖某个接口的纯 Python 实现，而事先并不知道究竟会覆盖哪些定义）。

  以这种方式重新发布名称时，下面关于公共接口和内部接口的指南仍然适用。

### 模块级双下划线名称

模块级“dunders”（即前后各有两个下划线的名称），例如 `__all__`、`__author__`、`__version__` 等，应放在模块文档字符串之后，但在任何导入语句之前，*除了* `from __future__` 导入。Python 要求 future 导入必须出现在模块中其他任何代码之前，文档字符串除外：

```python
"""This is the example module.

This module does stuff.
"""

from __future__ import barry_as_FLUFL

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

import os
import sys
```

## 字符串引号

在 Python 中，单引号字符串和双引号字符串相同。本 PEP 不就此作出推荐。选择一种规则并坚持使用。然而，当字符串包含单引号或双引号字符时，使用另一种引号以避免字符串中的反斜杠。这能提高可读性。

对于三引号字符串，始终使用双引号字符，以与 [PEP 257](https://peps.python.org/pep-0257/) 中的文档字符串约定保持一致。

## 表达式和语句中的空白

### 常见毛病

在以下情形中避免多余空白：

- 在圆括号、方括号或花括号内部紧贴处：

  **正确：**

  ```python
  spam(ham[1], {eggs: 2})
  ```

  **错误：**

  ```python
  spam( ham[ 1 ], { eggs: 2 } )
  ```

- 在尾随逗号与后续右圆括号之间：

  **正确：**

  ```python
  foo = (0,)
  ```

  **错误：**

  ```python
  bar = (0, )
  ```

- 在逗号、分号或冒号之前紧贴处：

  **正确：**

  ```python
  if x == 4: print(x, y); x, y = y, x
  ```

  **错误：**

  ```python
  if x == 4 : print(x , y) ; x , y = y , x
  ```

- 然而，在切片中，冒号像二元运算符一样起作用，两侧应有相同数量的空白（将其视为优先级最低的运算符）。在扩展切片中，两个冒号必须应用相同数量的空格。例外：当省略切片参数时，省略空格：

  **正确：**

  ```python
  ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
  ham[lower:upper], ham[lower:upper:], ham[lower::step]
  ham[lower+offset : upper+offset]
  ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
  ham[lower + offset : upper + offset]
  ```

  **错误：**

  ```python
  ham[lower + offset:upper + offset]
  ham[1: 9], ham[1 :9], ham[1:9 :3]
  ham[lower : : step]
  ham[ : upper]
  ```

- 在开始函数调用参数列表的左圆括号之前紧贴处：

  **正确：**

  ```python
  spam(1)
  ```

  **错误：**

  ```python
  spam (1)
  ```

- 在开始索引或切片的左圆括号之前紧贴处：

  **正确：**

  ```python
  dct['key'] = lst[index]
  ```

  **错误：**

  ```python
  dct ['key'] = lst [index]
  ```

- 在赋值（或其他）运算符周围使用多个空格以与另一行对齐：

  **正确：**

  ```python
  x = 1
  y = 2
  long_variable = 3
  ```

  **错误：**

  ```python
  x             = 1
  y             = 2
  long_variable = 3
  ```

### 其他建议

- 避免任何位置的尾随空白。因为它通常不可见，可能会令人困惑：例如，反斜杠后跟空格再跟换行符并不算作行续接标记。某些编辑器不会保留它，许多项目（如 CPython 本身）还有拒绝它的预提交钩子。

- 始终在这些二元运算符两侧各使用一个空格：赋值（`=`）、增强赋值（`+=`、`-=` 等）、比较（`==`、`<`、`>`、`!=`、`<=`、`>=`、`in`、`not in`、`is`、`is not`）、布尔运算（`and`、`or`、`not`）。

- 如果使用不同优先级的运算符，考虑在优先级最低的运算符周围添加空白。运用自己的判断；然而，绝不要使用多于一个空格，并且二元运算符两侧始终使用相同数量的空白：

  **正确：**

  ```python
  i = i + 1
  submitted += 1
  x = x*2 - 1
  hypot2 = x*x + y*y
  c = (a+b) * (a-b)
  ```

  **错误：**

  ```python
  i=i+1
  submitted +=1
  x = x * 2 - 1
  hypot2 = x * x + y * y
  c = (a + b) * (a - b)
  ```

- 函数注解应使用冒号的常规规则，并且如果存在 `->` 箭头，其周围始终有空格。（有关函数注解的更多内容，请参阅下文“函数注解”。）

  **正确：**

  ```python
  def munge(input: AnyStr): ...
  def munge() -> PosInt: ...
  ```

  **错误：**

  ```python
  def munge(input:AnyStr): ...
  def munge()->PosInt: ...
  ```

- 当 `=` 用于表示关键字参数，或用于表示*未注解*函数参数的默认值时，不要在 `=` 符号周围使用空格：

  **正确：**

  ```python
  def complex(real, imag=0.0):
      return magic(r=real, i=imag)
  ```

  **错误：**

  ```python
  def complex(real, imag = 0.0):
      return magic(r = real, i = imag)
  ```

  然而，当参数注解与默认值结合时，请在 `=` 符号周围使用空格：

  **正确：**

  ```python
  def munge(sep: AnyStr = None): ...
  def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...
  ```

  **错误：**

  ```python
  def munge(input: AnyStr=None): ...
  def munge(input: AnyStr, limit = 1000): ...
  ```

- 通常不鼓励复合语句（同一行上有多条语句）：

  **正确：**

  ```python
  if foo == 'blah':
      do_blah_thing()
  do_one()
  do_two()
  do_three()
  ```

  不建议：

  ```python
  if foo == 'blah': do_blah_thing()
  do_one(); do_two(); do_three()
  ```

- 虽然有时将 `if`/`for`/`while` 与小型主体放在同一行是可以的，但绝不要对多子句语句这样做。也要避免折叠这类长行！

  不建议：

  ```python
  if foo == 'blah': do_blah_thing()
  for x in lst: total += x
  while t < 10: t = delay()
  ```

  绝对不要：

  ```python
  if foo == 'blah': do_blah_thing()
  else: do_non_blah_thing()

  try: something()
  finally: cleanup()

  do_one(); do_two(); do_three(long, argument,
                               list, like, this)

  if foo == 'blah': one(); two(); three()
  ```

## 何时使用尾随逗号

尾随逗号通常是可选的，但在创建单元素元组时是必需的。为清晰起见，建议将后者放在（技术上多余的）圆括号中：

**正确：**

```python
FILES = ('setup.cfg',)
```

**错误：**

```python
FILES = 'setup.cfg',
```

当尾随逗号是冗余的时，在使用版本控制系统、并且预期值列表、参数列表或导入项列表会随时间扩展时，它们通常很有帮助。模式是将每个值（等）放在单独一行，始终添加尾随逗号，并将右圆括号/方括号/花括号放在下一行。然而，将尾随逗号与右定界符放在同一行没有意义（上述单元素元组情况除外）：

**正确：**

```python
FILES = [
    'setup.cfg',
    'tox.ini',
    ]
initialize(FILES,
           error=True,
           )
```

**错误：**

```python
FILES = ['setup.cfg', 'tox.ini',]
initialize(FILES, error=True,)
```

## 注释

与代码相矛盾的注释比没有注释更糟。代码变化时，始终优先保持注释最新！

注释应是完整句子。第一个单词应大写，除非它是以下小写字母开头的标识符（绝不要改变标识符的大小写！）。

块注释通常由一个或多个由完整句子构成的段落组成，每个句子以句号结尾。

在多句注释中，句子结束句号后应使用一个或两个空格，最后一句之后除外。

确保注释清晰，并且对于使用你所写语言的其他人来说易于理解。

来自非英语国家的 Python 程序员：请用英语写注释，除非你 120% 确定代码永远不会被不懂你语言的人阅读。

### 块注释

块注释通常适用于其后的一些（或全部）代码，并缩进到与该代码相同的层级。块注释的每一行都以 `#` 和一个空格开头（除非注释内部是缩进文本）。

块注释内的段落之间用仅包含一个 `#` 的行分隔。

### 行内注释

少用行内注释。

行内注释是与语句同一行的注释。行内注释应与语句至少相隔两个空格。它们应以 `#` 和一个空格开头。

行内注释如果陈述显而易见的内容，则是不必要的，事实上会分散注意力。不要这样做：

```python
x = x + 1                 # 将 x 加 1
```

但有时这样做是有用的：

```python
x = x + 1                 # 补偿边框
```

### 文档字符串

编写良好文档字符串（又称“docstrings”）的约定已固定于 [PEP 257](https://peps.python.org/pep-0257/)。

- 为所有公共模块、函数、类和方法编写文档字符串。非公共方法不需要文档字符串，但应有一条描述该方法作用的注释。此注释应出现在 `def` 行之后。

- [PEP 257](https://peps.python.org/pep-0257/) 描述了良好的文档字符串约定。最重要的是，结束多行文档字符串的 `"""` 应单独占一行：

  ```python
  """Return a foobang

  Optional plotz says to frobnicate the bizbaz first.
  """
  ```

- 对于单行文档字符串，请将结束的 `"""` 放在同一行：

  ```python
  """Return an ex-parrot."""
  ```

## 命名约定

Python 库的命名约定有些混乱，因此我们永远无法做到完全一致——不过，以下是当前推荐的命名标准。新模块和包（包括第三方框架）应按这些标准编写；但如果现有库有不同的风格，则优先保持内部一致性。

### 首要原则

对用户可见、作为 API 公共部分的名称，应遵循反映用法而非实现的约定。

### 描述性：命名风格

命名风格有很多种。能够独立于用途识别正在使用哪种命名风格是有帮助的。

通常区分以下命名风格：

- `b`（单个小写字母）
- `B`（单个大写字母）
- `lowercase`
- `lower_case_with_underscores`
- `UPPERCASE`
- `UPPER_CASE_WITH_UNDERSCORES`
- `CapitalizedWords`（或 CapWords，或 CamelCase——因其字母起伏的外观而得名 [^4]）。有时也称为 StudlyCaps。

  注意：在 CapWords 中使用缩略词时，将缩略词的所有字母大写。因此 `HTTPServerError` 优于 `HttpServerError`。

- `mixedCase`（与 CapitalizedWords 的区别是首字母小写！）
- `Capitalized_Words_With_Underscores`（难看！）

还有一种风格是使用短的唯一前缀将相关名称分组。这在 Python 中不常用，但为完整起见提及。例如，`os.stat()` 函数返回一个元组，其各项传统上命名为 `st_mode`、`st_size`、`st_mtime` 等。（这样做是为了强调与 POSIX 系统调用结构体字段的对应关系，帮助熟悉该结构体的程序员。）

X11 库为其所有公共函数使用前导 `X`。在 Python 中，这种风格通常被认为没有必要，因为属性和方法名以对象为前缀，函数名以模块名为前缀。

此外，还识别以下使用前导或尾随下划线的特殊形式（通常可以与任何大小写约定组合）：

- `_single_leading_underscore`：弱“内部使用”指示符。例如，`from M import *` 不会导入名称以下划线开头的对象。

- `single_trailing_underscore_`：按约定用于避免与 Python 关键字冲突，例如：

  ```python
  tkinter.Toplevel(master, class_='ClassName')
  ```

- `__double_leading_underscore`：命名类属性时，会触发名称改写（在类 `FooBar` 内部，`__boo` 变为 `_FooBar__boo`；见下文）。

- `__double_leading_and_trailing_underscore__`：存在于用户控制命名空间中的“魔法”对象或属性。例如 `__init__`、`__import__` 或 `__file__`。绝不要发明这类名称；只按文档使用它们。

### 规定性：命名约定

#### 应避免的名称

绝不要将字符 `l`（小写字母 el）、`O`（大写字母 oh）或 `I`（大写字母 eye）用作单字符变量名。

在某些字体中，这些字符与数字 1 和 0 无法区分。当想使用 `l` 时，改用 `L`。

#### ASCII 兼容性

标准库中使用的标识符必须如 [PEP 3131 的策略部分](https://peps.python.org/pep-3131/#policy-specification)所述，与 ASCII 兼容。

#### 包和模块名

模块应使用简短的全小写名称。如果下划线能提高可读性，可以在模块名中使用下划线。Python 包也应使用简短的全小写名称，尽管不鼓励使用下划线。

当用 C 或 C++ 编写的扩展模块有配套的 Python 模块提供更高层（例如更面向对象）接口时，C/C++ 模块带前导下划线（例如 `_socket`）。

#### 类名

类名通常应使用 CapWords 约定。

在接口已有文档说明且主要作为可调用对象使用的情况下，可以改用函数命名约定。

注意，内置名称有单独的约定：大多数内置名称是单个单词（或两个单词连在一起），CapWords 约定仅用于异常名和内置常量。

#### 类型变量名

[PEP 484](https://peps.python.org/pep-0484/) 引入的类型变量名通常应使用 CapWords，并优先使用短名称：`T`、`AnyStr`、`Num`。建议为用于声明协变或逆变行为的变量分别添加后缀 `_co` 或 `_contra`：

```python
from typing import TypeVar

VT_co = TypeVar('VT_co', covariant=True)
KT_contra = TypeVar('KT_contra', contravariant=True)
```

#### 异常名

由于异常应是类，因此这里适用类命名约定。然而，如果异常确实是错误，应在异常名后加上后缀 `Error`。

#### 全局变量名

（我们希望这些变量只在一个模块内部使用。）其约定与函数名大致相同。

设计为通过 `from M import *` 使用的模块，应使用 `__all__` 机制防止导出全局变量，或使用较旧的约定：为此类全局变量加前导下划线（你可能想这样做以表明这些全局变量是“模块非公共的”）。

#### 函数和变量名

函数名应小写，必要时用下划线分隔单词以提高可读性。

变量名遵循与函数名相同的约定。

只有在已是主流风格的上下文中（例如 `threading.py`），才允许使用 mixedCase，以保持向后兼容性。

#### 函数和方法参数

实例方法的第一个参数始终使用 `self`。

类方法的第一个参数始终使用 `cls`。

如果函数参数名与保留关键字冲突，通常最好追加一个尾随下划线，而不是使用缩写或拼写变形。因此 `class_` 优于 `clss`。（也许更好的是使用同义词来避免此类冲突。）

#### 方法名和实例变量

使用函数命名规则：小写，必要时用下划线分隔单词以提高可读性。

仅对非公共方法和实例变量使用一个前导下划线。

为避免与子类发生名称冲突，使用两个前导下划线以调用 Python 的名称改写规则。

Python 会用类名改写这些名称：如果类 `Foo` 有一个名为 `__a` 的属性，则不能通过 `Foo.__a` 访问它。（执着的用户仍可通过调用 `Foo._Foo__a` 访问。）通常，双前导下划线只应用于避免设计为可被继承的类中的属性发生名称冲突。

注意：关于 `__names` 的使用存在一些争议（见下文）。

#### 常量

常量通常在模块级定义，并以全大写字母书写，单词之间用下划线分隔。示例包括 `MAX_OVERFLOW` 和 `TOTAL`。

#### 面向继承设计

始终决定类的方法和实例变量（统称“属性”）应是公共还是非公共。拿不准时，选择非公共；以后将非公共属性改为公共，比将公共属性改为非公共更容易。

公共属性是你期望类的无关客户端使用的属性，并且你承诺避免向后不兼容的更改。非公共属性是不打算供第三方使用的属性；你不保证非公共属性不会变化甚至不会被移除。

这里不使用“私有”一词，因为在 Python 中（除非进行通常不必要的额外工作）没有属性真正是私有的。

另一类属性是“子类 API”的一部分（在其他语言中常称为“受保护”）。有些类设计为可被继承，以扩展或修改类行为的某些方面。设计此类类时，要注意明确决定哪些属性是公共的、哪些是子类 API 的一部分、哪些真正只供基类使用。

基于此，以下是 Pythonic 指南：

- 公共属性不应有前导下划线。

- 如果公共属性名与保留关键字冲突，请在属性名后追加一个尾随下划线。这比使用缩写或拼写变形更可取。（然而，尽管有此规则，对于任何已知为类的变量或参数，尤其是类方法的第一个参数，`cls` 是首选拼写。）

  注意 1：请参阅上文关于类方法参数名的建议。

- 对于简单的公共数据属性，最好只暴露属性名，不使用复杂的访问器/修改器方法。请记住，如果你发现简单数据属性需要增加功能行为，Python 提供了轻松的后续增强路径。在这种情况下，使用属性（property）将功能实现隐藏在简单的数据属性访问语法之后。

  注意 1：尽量保持功能行为无副作用，不过缓存之类的副作用通常是可以的。

  注意 2：避免将属性用于计算开销很大的操作；属性表示法会让调用者认为访问（相对）廉价。

- 如果你的类打算被继承，并且有些属性你不希望子类使用，考虑将它们命名为双前导下划线且无尾随下划线。这会调用 Python 的名称改写算法，将类名改写进属性名。这有助于避免子类无意中包含同名属性时发生属性名冲突。

  注意 1：注意，改写后的名称只使用简单类名，因此如果子类选择相同的类名和属性名，仍可能发生名称冲突。

  注意 2：名称改写会使某些用途（例如调试和 `__getattr__()`）不太方便。然而，名称改写算法有详细文档，且易于手动执行。

  注意 3：并非所有人都喜欢名称改写。请尽量在避免意外名称冲突的需要与高级调用者潜在使用之间取得平衡。

### 公共接口和内部接口

任何向后兼容性保证仅适用于公共接口。因此，用户能够清楚区分公共接口和内部接口很重要。

有文档记录的接口被视为公共接口，除非文档明确声明它们是暂定的或内部接口，不受通常的向后兼容性保证约束。所有未记录接口都应假定为内部接口。

为了更好地支持内省，模块应使用 `__all__` 属性显式声明其公共 API 中的名称。将 `__all__` 设置为空列表表示模块没有公共 API。

即使适当设置了 `__all__`，内部接口（包、模块、类、函数、属性或其他名称）仍应加一个前导下划线。

如果任何包含命名空间（包、模块或类）被视为内部接口，则该接口也被视为内部接口。

导入的名称应始终视为实现细节。其他模块不得依赖对此类导入名称的间接访问，除非它们是包含模块 API 中明确记录的一部分，例如 `os.path`，或包的 `__init__` 模块暴露子模块功能。

## 编程建议

- 代码编写方式不应不利于 Python 的其他实现（PyPy、Jython、IronPython、Cython、Psyco 等）。

  例如，不要依赖 CPython 对 `a += b` 或 `a = a + b` 形式语句的高效原地字符串拼接实现。这种优化即使在 CPython 中也很脆弱（仅对某些类型有效），而在不使用引用计数的实现中根本不存在。在库的性能敏感部分，应改用 `''.join()` 形式。这将确保在各种实现中拼接都以线性时间进行。

- 与 `None` 等单例的比较应始终使用 `is` 或 `is not`，绝不要使用相等运算符。

  另外，当真正意思是 `if x is not None` 时，要小心写成 `if x`——例如，在测试一个默认值为 `None` 的变量或参数是否被设置为其他值时。其他值可能具有在布尔上下文中为假的类型（例如容器）！

- 使用 `is not` 运算符，而不是 `not ... is`。虽然两个表达式功能相同，但前者更可读，更受偏好：

  **正确：**

  ```python
  if foo is not None:
  ```

  **错误：**

  ```python
  if not foo is None:
  ```

- 使用富比较实现排序操作时，最好实现全部六个操作（`__eq__`、`__ne__`、`__lt__`、`__le__`、`__gt__`、`__ge__`），而不是依赖其他代码只使用某个特定比较。

  为尽量减少工作量，`functools.total_ordering()` 装饰器提供了生成缺失比较方法的工具。

  [PEP 207](https://peps.python.org/pep-0207/) 指出 Python *确实*假定自反性规则。因此，解释器可以将 `y > x` 与 `x < y` 互换，将 `y >= x` 与 `x <= y` 互换，并可以交换 `x == y` 和 `x != y` 的参数。`sort()` 和 `min()` 操作保证使用 `<` 运算符，`max()` 函数使用 `>` 运算符。然而，最好实现全部六个操作，以免在其他上下文中引起混淆。

- 始终使用 `def` 语句，而不是将 `lambda` 表达式直接绑定到标识符的赋值语句：

  **正确：**

  ```python
  def f(x): return 2*x
  ```

  **错误：**

  ```python
  f = lambda x: 2*x
  ```

  第一种形式意味着结果函数对象的名称具体为 `f`，而不是通用的 `<lambda>`。这通常对回溯和字符串表示更有用。使用赋值语句消除了 `lambda` 表达式相对于显式 `def` 语句的唯一优势（即它可以嵌入更大的表达式中）。

- 异常应从 `Exception` 派生，而不是从 `BaseException` 派生。直接从 `BaseException` 继承保留给捕获它们几乎总是错误做法的情况。

  根据*捕获*异常的代码可能需要的区分来设计异常层次结构，而不是根据抛出异常的位置。目标是程序化地回答“出了什么问题？”，而不仅仅是说明“发生了问题”（有关内置异常层次结构吸取此教训的示例，请参阅 [PEP 3151](https://peps.python.org/pep-3151/)）。

  这里适用类命名约定，不过如果异常是错误，应在异常类后添加后缀 `Error`。用于非局部流控制或其他信号形式的非错误异常不需要特殊后缀。

- 适当使用异常链。应使用 `raise X from Y` 表示显式替换而不丢失原始回溯。

  当故意替换内部异常时（使用 `raise X from None`），确保将相关细节转移到新异常中（例如将 `KeyError` 转换为 `AttributeError` 时保留属性名，或将原始异常的文本嵌入新异常消息中）。

- 捕获异常时，尽可能提及具体异常，而不是使用裸 `except:` 子句：

  ```python
  try:
      import platform_specific_module
  except ImportError:
      platform_specific_module = None
  ```

  裸 `except:` 子句会捕获 `SystemExit` 和 `KeyboardInterrupt` 异常，使程序更难通过 Control-C 中断，并可能掩盖其他问题。如果你想捕获所有表示程序错误的异常，请使用 `except Exception:`（裸 `except` 等价于 `except BaseException:`）。

  一个好的经验法则是将裸 `except` 子句的使用限制在两种情况下：

  1. 如果异常处理程序将打印或记录回溯；至少用户会知道发生了错误。
  2. 如果代码需要做一些清理工作，但随后用 `raise` 让异常向上传播。`try...finally` 可能是处理这种情况的更好方式。

- 捕获操作系统错误时，优先使用 Python 3.3 引入的显式异常层次结构，而不是对 `errno` 值进行内省。

- 此外，对于所有 `try/except` 子句，将 `try` 子句限制为必要的最小代码量。这同样可以避免掩盖错误：

  **正确：**

  ```python
  try:
      value = collection[key]
  except KeyError:
      return key_not_found(key)
  else:
      return handle_value(value)
  ```

  **错误：**

  ```python
  try:
      # 范围太宽！
      return handle_value(collection[key])
  except KeyError:
      # 也会捕获 handle_value() 抛出的 KeyError
      return key_not_found(key)
  ```

- 当资源局限于代码的特定区段时，使用 `with` 语句确保使用后及时可靠地清理。`try/finally` 语句也可接受。

- 当上下文管理器执行的操作不只是获取和释放资源时，应通过单独的函数或方法调用：

  **正确：**

  ```python
  with conn.begin_transaction():
      do_stuff_in_transaction(conn)
  ```

  **错误：**

  ```python
  with conn:
      do_stuff_in_transaction(conn)
  ```

  后一个示例没有提供任何信息表明 `__enter__` 和 `__exit__` 方法除了在事务后关闭连接之外还做了其他事情。在这种情况下，显式表达很重要。

- 在返回语句中保持一致。函数中的所有返回语句要么都返回表达式，要么都不返回。如果任何返回语句返回表达式，则任何不返回值的返回语句都应显式写为 `return None`，并且如果可达，函数末尾应存在显式返回语句：

  **正确：**

  ```python
  def foo(x):
      if x >= 0:
          return math.sqrt(x)
      else:
          return None

  def bar(x):
      if x < 0:
          return None
      return math.sqrt(x)
  ```

  **错误：**

  ```python
  def foo(x):
      if x >= 0:
          return math.sqrt(x)

  def bar(x):
      if x < 0:
          return
      return math.sqrt(x)
  ```

- 使用 `''.startswith()` 和 `''.endswith()` 检查前缀或后缀，而不是字符串切片。

  `startswith()` 和 `endswith()` 更清晰，更不容易出错：

  **正确：**

  ```python
  if foo.startswith('bar'):
  ```

  **错误：**

  ```python
  if foo[:3] == 'bar':
  ```

- 对象类型比较应始终使用 `isinstance()`，而不是直接比较类型：

  **正确：**

  ```python
  if isinstance(obj, int):
  ```

  **错误：**

  ```python
  if type(obj) is type(1):
  ```

- 对于序列（字符串、列表、元组），利用空序列为假这一事实：

  **正确：**

  ```python
  if not seq:
  if seq:
  ```

  **错误：**

  ```python
  if len(seq):
  if not len(seq):
  ```

- 不要编写依赖重要尾随空白的字符串字面量。这种尾随空白在视觉上无法区分，某些编辑器（或较新的 `reindent.py`）会将其修剪掉。

- 不要使用 `==` 将布尔值与 `True` 或 `False` 比较：

  **正确：**

  ```python
  if greeting:
  ```

  **错误：**

  ```python
  if greeting == True:
  ```

  更糟：

  **错误：**

  ```python
  if greeting is True:
  ```

- 不鼓励在 `try...finally` 的 `finally` 套件中使用流控制语句 `return`/`break`/`continue`，因为此类语句会跳出 `finally` 套件。这是因为此类语句会隐式取消正在通过 `finally` 套件传播的任何活动异常：

  **错误：**

  ```python
  def foo():
      try:
          1 / 0
      finally:
          return 42
  ```

### 函数注解

随着 [PEP 484](https://peps.python.org/pep-0484/) 被接受，函数注解的风格规则已经改变。

- 函数注解应使用 [PEP 484](https://peps.python.org/pep-0484/) 语法（上一节中有一些关于注解的格式建议）。

- 本 PEP 之前推荐的注解风格实验不再鼓励。

- 然而，在标准库之外，现在鼓励在 [PEP 484](https://peps.python.org/pep-0484/) 规则内进行实验。例如，用 [PEP 484](https://peps.python.org/pep-0484/) 风格类型注解标记大型第三方库或应用，审查添加这些注解有多容易，并观察它们的存在是否提高代码可理解性。

- Python 标准库在采用此类注解时应保持保守，但允许在新代码和大型重构中使用它们。

- 对于希望以不同方式使用函数注解的代码，建议在文件顶部附近放置如下形式的注释：

  ```python
  # type: ignore
  ```

  这会告诉类型检查器忽略所有注解。（有关禁用类型检查器抱怨的更细粒度方法，请参阅 [PEP 484](https://peps.python.org/pep-0484/)。）

- 与 linter 一样，类型检查器是可选的独立工具。Python 解释器默认不应因类型检查而发出任何消息，也不应基于注解改变行为。

- 不想使用类型检查器的用户完全可以忽略它们。然而，预期第三方库包的用户可能希望对这些包运行类型检查器。为此，[PEP 484](https://peps.python.org/pep-0484/) 建议使用存根文件：类型检查器优先读取的 `.pyi` 文件，而不是对应的 `.py` 文件。存根文件可以与库一起分发，或在库作者许可下通过 typeshed 仓库单独分发 [^5]。

### 变量注解

[PEP 526](https://peps.python.org/pep-0526/) 引入了变量注解。其风格建议与上述函数注解类似：

- 模块级变量、类和实例变量以及局部变量的注解，冒号后应有一个空格。

- 冒号前不应有空格。

- 如果赋值有右侧，则等号两侧应恰好各有一个空格：

  **正确：**

  ```python
  code: int

  class Point:
      coords: Tuple[int, int]
      label: str = '<unknown>'
  ```

  **错误：**

  ```python
  code:int  # 冒号后没有空格
  code : int  # 冒号前有空格

  class Test:
      result: int=0  # 等号两侧没有空格
  ```

- 尽管 [PEP 526](https://peps.python.org/pep-0526/) 是为 Python 3.6 接受的，但变量注解语法是所有 Python 版本上存根文件的首选语法（详情请参阅 [PEP 484](https://peps.python.org/pep-0484/)）。

## 脚注

[^fn-hi]: *悬挂缩进*是一种排版风格，其中段落中除第一行外的所有行都缩进。在 Python 语境中，该术语用于描述这样一种风格：带圆括号语句的左圆括号是行末最后一个非空白字符，后续行缩进，直到右圆括号。

[^2]: Barry 的 GNU Mailman 风格指南：<http://barry.warsaw.us/software/STYLEGUIDE.txt>

[^3]: Donald Knuth 的 *The TeXBook*，第 195 和 196 页。

[^4]: <http://www.wikipedia.com/wiki/Camel_case>

[^5]: Typeshed 仓库：<https://github.com/python/typeshed>

## 版权

本文档已置于公共领域。