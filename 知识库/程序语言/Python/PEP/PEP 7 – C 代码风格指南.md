https://peps.python.org/pep-0007/

# PEP 7 – C 代码风格指南

| 项目 | 内容 |
| --- | --- |
| PEP | 7 |
| 标题 | C 代码风格指南 |
| 作者 | Guido van Rossum &lt;guido@python.org&gt;、Barry Warsaw &lt;barry@python.org&gt; |
| 状态 | 活跃 |
| 类型 | 流程 |
| 创建日期 | 2001-07-05 |
| 历史记录 | 无 |

## 引言

本文档给出构成 Python C 实现的 C 代码的编码约定。另请参阅配套的信息性 PEP：[Python 代码风格指南（PEP 8）](https://peps.python.org/pep-0008/)。

注意，规则就是用来打破的。打破某条特定规则有两个好理由：

1. 应用该规则会使代码可读性降低，即使对习惯阅读遵循规则代码的人也是如此。
2. 为了与同样打破该规则的周围代码保持一致（可能是历史原因）——不过这也是清理他人遗留问题的机会（真正的极限编程（XP）风格）。

## C 标准

遵循以下标准。对于相关标准中未包含的特性，使用 CPython 专用包装（例如：`_Py_atomic_store_int32`、`Py_ALWAYS_INLINE`、`Py_ARITHMETIC_RIGHT_SHIFT`；公共头文件中的 `_Py_ALIGNED_DEF`）。添加此类包装时，尽量使其易于针对不受支持的编译器进行调整。

* Python 3.11 及更新版本使用 C11（不含[可选特性](https://en.wikipedia.org/wiki/C11_%28C_standard_revision%29#Optional_features)）。公共 C API 应兼容 C99 和 C++。

  （提醒阅读本文的用户：本 PEP 是*风格指南*；这些规则就是用来打破的。）

* Python 3.6 到 3.10 使用 C89，并选用若干 C99 特性：

  * `<stdint.h>` 和 `<inttypes.h>` 中的标准整数类型。我们需要固定宽度整数类型。
  * `static inline` 函数
  * 指定初始化器（尤其适合类型声明）
  * 声明可与其他语句交错
  * 布尔类型
  * C++ 风格行注释

* Python 3.6 之前的版本使用 ANSI/ISO 标准 C（1989 年版标准）。这意味着，除许多其他事项外，所有声明都必须位于块的开头。

## 通用 C 代码约定

* 不要使用编译器特定扩展，例如 GCC 或 MSVC 的扩展。例如，不要编写不带行尾反斜杠的多行字符串。
* 所有函数声明和定义都必须使用完整原型。也就是说，指定所有参数的类型，并使用 `(void)` 声明无参数的函数。
* 主要编译器（gcc、VC++ 及其他若干编译器）不应产生编译器警告。
* 在新代码中，`static inline` 函数应优先于宏。

## 代码布局

* 使用 4 空格缩进，完全不使用制表符。
* 任何行不得超过 79 个字符。如果此规则与上一条规则合在一起仍不足以让你编写代码，说明代码太复杂——考虑拆分为子例程。
* 任何行都不应以空白字符结尾。如果你认为自己需要有意义的行尾空白，请再想想——别人的编辑器可能会例行删除它。
* 函数定义风格：函数名位于第 1 列，最外层花括号位于第 1 列，局部变量声明后空一行。

**正确：**

```c
static int
extra_ivars(PyTypeObject *type, PyTypeObject *base)
{
    int t_size = PyType_BASICSIZE(type);
    int b_size = PyType_BASICSIZE(base);

    assert(t_size >= b_size); /* type smaller than base! */
    ...
    return 1;
}
```

* 代码结构：关键字（如 `if`、`for`）与后面的左括号之间有一个空格；括号内不加空格；所有地方都要求花括号，即使 C 允许省略；但不要给并非因其他原因修改的代码添加花括号。所有新的 C 代码都要求使用花括号。花括号格式如下：

**正确：**

```c
if (mro != NULL) {
    ...
}
else {
    ...
}
```

* `return` 语句不应添加冗余括号：

**错误：**

```c
return(albatross); /* 错误 */
```

应改为：

**正确：**

```c
return albatross; /* 正确 */
```

* 函数和宏调用风格：`foo(a, b, c)`——左括号前不加空格，括号内不加空格，逗号前不加空格，每个逗号后加一个空格。
* 始终在赋值、布尔和比较运算符两侧加空格。在运算符很多的表达式中，在最外层（最低优先级）运算符两侧加空格。
* 长行断行：如果可能，在最外层参数列表的逗号后断行。始终适当缩进续行，例如：

**正确：**

```c
PyErr_Format(PyExc_TypeError,
             "cannot create '%.100s' instances",
             type->tp_name);
```

* 当在二元运算符处断开长表达式时，花括号应如下格式化：

**正确：**

```c
if (type->tp_dictoffset != 0
    && base->tp_dictoffset == 0
    && type->tp_dictoffset == b_size
    && (size_t)t_size == b_size + sizeof(PyObject *))
{
    return 0; /* "Forgive" adding a __dict__ only */
}
```

将运算符放在行尾也可以，尤其是为了与周围代码保持一致。（关于更长的讨论，参见 [PEP 8 中关于二元运算符换行的讨论](https://peps.python.org/pep-0008/#should-a-line-break-before-or-after-a-binary-operator)。）

* 在多行宏中，将续行字符垂直对齐。
* 打算作为语句使用的宏应使用 `do { ... } while (0)` 宏惯用法，末尾不加分号。示例：

**正确：**

```c
#define ADD_INT_MACRO(MOD, INT)                                   \
    do {                                                          \
        if (PyModule_AddIntConstant((MOD), (#INT), (INT)) < 0) {  \
            goto error;                                           \
        }                                                         \
    } while (0)

// To be used like a statement with a semicolon:
ADD_INT_MACRO(m, SOME_CONSTANT);
```

* 使用完毕后，对文件局部宏执行 `#undef`。
* 在函数、结构定义以及函数内的主要部分周围留空行。
* 注释放在其所描述代码之前。
* 所有函数和全局变量都应声明为 `static`，除非它们要作为已发布接口的一部分。
* 对于外部函数和变量，我们总是在 `Include` 目录中的适当头文件里提供声明，并使用 `PyAPI_FUNC()` 宏和 `PyAPI_DATA()` 宏，如下所示：

**正确：**

```c
PyAPI_FUNC(PyObject *) PyObject_Repr(PyObject *);

PyAPI_DATA(PyTypeObject) PySuper_Type;
```

## 命名约定

* 公共函数使用 `Py` 前缀；静态函数绝不使用该前缀。`Py_` 前缀保留给全局服务例程，如 `Py_FatalError`；特定例程组（例如特定对象类型 API）使用更长前缀，例如字符串函数使用 `PyString_`。
* 公共函数和变量使用混合大小写并带下划线，例如：`PyObject_GetAttr`、`Py_BuildValue`、`PyExc_TypeError`。
* 偶尔“内部”函数需要让加载器可见；我们为此使用 `_Py` 前缀，例如：`_PyObject_Dump`。
* 宏应使用混合大小写前缀，随后使用大写，例如：`PyString_AS_STRING`、`Py_PRINT_RAW`。
* 宏参数应使用 `ALL_CAPS` 风格，以便与 C 变量和结构成员轻松区分。

## 文档字符串

* 使用 `PyDoc_STR()` 或 `PyDoc_STRVAR()` 宏来编写文档字符串，以支持构建不带文档字符串的 Python（`./configure --without-doc-strings`）。
* 每个函数文档字符串的第一行应为“签名行”，简要概述参数和返回值。例如：

**正确：**

```c
PyDoc_STRVAR(myfunction__doc__,
"myfunction(name, value) -> bool\n\n\
Determine whether name and value make a valid pair.");
```

始终在签名行与描述文本之间包含一个空行。

如果函数的返回值始终为 `None`（因为没有有意义的返回值），则不要包含返回类型说明。

* 编写多行文档字符串时，务必始终使用反斜杠续行，如上例所示，或使用字符串字面量拼接：

**正确：**

```c
PyDoc_STRVAR(myfunction__doc__,
"myfunction(name, value) -> bool\n\n"
"Determine whether name and value make a valid pair.");
```

尽管有些 C 编译器接受两者都不使用的字符串字面量：

**错误：**

```c
/* BAD -- don't do this! */
PyDoc_STRVAR(myfunction__doc__,
"myfunction(name, value) -> bool\n\n
Determine whether name and value make a valid pair.");
```

但并非所有编译器都如此；已知 MSVC 编译器会对此报错。

## 版权

本文档已置于公共领域。