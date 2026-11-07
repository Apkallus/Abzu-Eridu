https://jinja.palletsprojects.com/en/stable/templates/

# 模板设计器文档

本文档描述模板引擎的语法和语义，对于创建 Jinja 模板的人员来说，它将是最有用的参考。由于模板引擎非常灵活，应用程序的配置在分隔符和未定义值的行为方面可能与本文件所呈现的代码略有不同。

## 概要

Jinja 模板只是一个文本文件。Jinja 可以生成任何基于文本的格式（HTML、XML、CSV、LaTeX 等）。Jinja 模板不需要具有特定扩展名：`.html`、`.xml` 或任何其他扩展名都可以。

模板包含**变量**和/或**表达式**，它们在模板被*渲染*时会被替换为值；还包含**标签**，用于控制模板逻辑。模板语法深受 Django 和 Python 启发。

下面是一个最小模板，使用默认 Jinja 配置说明了一些基础知识。本文档稍后将介绍细节：

```jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Webpage</title>
</head>
<body>
    <ul id="navigation">
    {% for item in navigation %}
        <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
    </ul>

    <h1>My Webpage</h1>
    {{ a_variable }}

    {# 一条注释 #}
</body>
</html>
```

以下示例展示了默认配置设置。应用程序开发者可以将语法配置从 `{% foo %}` 改为 `<% foo %>` 或类似形式。

有几种分隔符。默认 Jinja 分隔符配置如下：

- `{% ... %}` 用于[语句]
- `{{ ... }}` 用于[表达式]，打印到模板输出
- `{# ... #}` 用于[注释]，不包含在模板输出中

也可以使用[行语句和注释]，不过它们没有默认前缀字符。要使用它们，在创建 [Environment] 时设置 `line_statement_prefix` 和 `line_comment_prefix`。

### 模板文件扩展名

如上所述，任何文件都可以作为模板加载，无论文件扩展名如何。添加 `.jinja` 扩展名（如 `user.html.jinja`）可能使某些 IDE 或编辑器插件更容易识别，但并非必需。后面介绍的自动转义可以基于文件扩展名应用，因此在这种情况下需要考虑额外的后缀。

识别模板的另一个好方法是：无论扩展名如何，它们都位于 `templates` 文件夹中。这是项目的常见布局。

## 变量

模板变量由传递给模板的上下文字典定义。

只要变量由应用程序传入，你就可以在模板中随意使用它们。变量可能具有属性或元素，你也可以访问它们。变量具有哪些属性很大程度上取决于提供该变量的应用程序。

除了标准的 Python `__getitem__` “下标”语法（`[]`）之外，你还可以使用点（`.`）访问变量的属性。

以下两行作用相同：

```jinja
{{ foo.bar }}
{{ foo['bar'] }}
```

重要的是要知道，外层双花括号*不是*变量的一部分，而是打印语句。如果你在标签内访问变量，不要在它们周围加花括号。

如果变量或属性不存在，你将得到一个未定义值。你可以对该值做什么取决于应用程序配置：默认行为是，如果打印或迭代它，则求值为空字符串；对于其他所有操作则失败。

> **实现**
>
> 为方便起见，Jinja 中的 `foo.bar` 在 Python 层执行以下操作：
>
> - 检查 `foo` 上是否存在名为 `bar` 的属性（`getattr(foo, 'bar')`）
> - 如果不存在，检查 `foo` 中是否存在项 `'bar'`（`foo.__getitem__('bar')`）
> - 如果不存在，返回一个未定义对象。
>
> `foo['bar']` 的工作方式大致相同，只是顺序略有不同：
>
> - 检查 `foo` 中是否存在项 `'bar'`（`foo.__getitem__('bar')`）
> - 如果不存在，检查 `foo` 上是否存在名为 `bar` 的属性（`getattr(foo, 'bar')`）
> - 如果不存在，返回一个未定义对象。
>
> 如果对象具有同名的项和属性，这一点很重要。此外，`attr()` 过滤器只查找属性。

## 过滤器

变量可以通过**过滤器**修改。过滤器与变量之间用管道符号（`|`）分隔，并且可以在括号中带有可选参数。多个过滤器可以链式调用。一个过滤器的输出会应用到下一个过滤器。

例如，`{{ name|striptags|title }}` 将从变量 `name` 中移除所有 HTML 标签，并将输出转换为标题大小写（`title(striptags(name))`）。

接受参数的过滤器在参数周围有括号，就像函数调用一样。例如：`{{ listx|join(', ') }}` 将用逗号连接列表（`str.join(', ', listx)`）。

下面的[内置过滤器列表]描述了所有内置过滤器。

## 测试

除了过滤器之外，还有所谓的“测试”可用。测试可用于针对常见表达式测试变量。要测试变量或表达式，在变量后添加 `is` 加上测试名称。例如，要判断变量是否已定义，可以执行 `name is defined`，这将根据当前模板上下文中是否定义了 `name` 返回真或假。

测试也可以接受参数。如果测试只接受一个参数，可以省略括号。例如，以下两个表达式作用相同：

```jinja
{% if loop.index is divisibleby 3 %}
{% if loop.index is divisibleby(3) %}
```

下面的[内置测试列表]描述了所有内置测试。

## 注释

要注释掉模板中的部分行，使用注释语法，默认设置为 `{# ... #}`。这对于在调试时注释掉模板的某些部分，或为其他模板设计者或你自己添加信息很有用：

```jinja
{# 注意：注释掉的模板，因为我们不再使用它
    {% for user in users %}
        ...
    {% endfor %}
#}
```

## 空白控制

在默认配置中：

- 如果存在单个尾随换行符，则将其去除
- 其他空白（空格、制表符、换行符等）原样返回

如果应用程序将 Jinja 配置为 `trim_blocks`，则模板标签后的第一个换行符会自动移除（就像 PHP 中那样）。还可以设置 `lstrip_blocks` 选项，以去除从行首到块开始处的制表符和空格。（如果块开始前有其他字符，则不会去除任何内容。）

在同时禁用 `trim_blocks` 和 `lstrip_blocks`（默认）的情况下，单独成行的块标签将被移除，但会保留一个空行，并且内容中的空格会保留。例如，以下模板：

```jinja
<div>
    {% if True %}
        yay
    {% endif %}
</div>
```

在同时禁用 `trim_blocks` 和 `lstrip_blocks` 的情况下，模板渲染结果中 div 内会有空行：

```text
<div>

        yay

</div>
```

在同时启用 `trim_blocks` 和 `lstrip_blocks` 的情况下，模板块行会被完全移除：

```text
<div>
        yay
</div>
```

你可以通过在块开头放置加号（`+`）来手动禁用 `lstrip_blocks` 行为：

```jinja
<div>
        {%+ if something %}yay{% endif %}
</div>
```

同样，你可以通过在块末尾放置加号（`+`）来手动禁用 `trim_blocks` 行为：

```jinja
<div>
    {% if something +%}
        yay
    {% endif %}
</div>
```

你也可以手动去除模板中的空白。如果在块（例如 [For] 标签）、注释或变量表达式的开头或结尾添加减号（`-`），则该块之前或之后的空白将被移除：

```jinja
{% for item in seq -%}
    {{ item }}
{%- endfor %}
```

这将输出所有元素，且它们之间没有空白。如果 `seq` 是 `1` 到 `9` 的数字列表，输出将是 `123456789`。

如果启用了[行语句]，它们会自动去除行首到行首开始处的空白。

默认情况下，Jinja 还会移除尾随换行符。要保留单个尾随换行符，将 Jinja 配置为 `keep_trailing_newline`。

> **注意**
>
> 不得在标签和减号之间添加空白。
>
> **有效**：
>
> ```jinja
> {%- if foo -%}...{% endif %}
> ```
>
> **无效**：
>
> ```jinja
> {% - if foo - %}...{% endif %}
> ```

## 转义

有时希望——甚至需要——让 Jinja 忽略它原本会作为变量或块处理的部分。例如，如果使用默认语法，你想在模板中将 `{{` 用作原始字符串而不启动变量，就必须使用一个技巧。

输出字面变量分隔符（`{{`）的最简单方法是使用变量表达式：

```jinja
{{ '{{' }}
```

对于更大的片段，将块标记为 `raw` 是合理的。例如，要在模板中包含 Jinja 语法示例，可以使用以下片段：

```jinja
{% raw %}
    <ul>
    {% for item in seq %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
{% endraw %}
```

> **注意**
>
> `{% raw -%}` 标签末尾的减号会清除原始数据第一个字符之前的所有空格和换行。

## 行语句

如果应用程序启用了行语句，就可以将一行标记为语句。例如，如果行语句前缀配置为 `#`，以下两个示例等价：

```jinja
<ul>
# for item in seq
    <li>{{ item }}</li>
# endfor
</ul>

<ul>
{% for item in seq %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

行语句前缀可以出现在行上的任何位置，只要它前面没有文本。为了提高可读性，开始一个块的语句（如 `for`、`if`、`elif` 等）可以以冒号结尾：

```jinja
# for item in seq:
    ...
# endfor
```

> **注意**
>
> 如果有未闭合的圆括号、花括号或方括号，行语句可以跨越多行：
>
> ```jinja
> <ul>
> # for href, caption in [('index.html', 'Index'),
>                         ('about.html', 'About')]:
>     <li><a href="{{ href }}">{{ caption }}</a></li>
> # endfor
> </ul>
> ```

自 Jinja 2.2 起，也可以使用基于行的注释。例如，如果行注释前缀配置为 `##`，则从 `##` 到行尾的所有内容都会被忽略（不包括换行符）：

```jinja
# for item in seq:
    <li>{{ item }}</li>     ## 此注释被忽略
# endfor
```

## 模板继承

Jinja 最强大的部分是模板继承。模板继承允许你构建一个基础“骨架”模板，其中包含站点的所有常见元素，并定义子模板可以覆盖的**块**。

听起来复杂，但其实非常基础。通过一个示例来理解是最容易的。

### 基础模板

这个模板我们称为 `base.html`，定义了一个简单的 HTML 骨架文档，可用于简单的两栏页面。“子”模板的工作是用内容填充空块：

```jinja
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}{% endblock %} - My Webpage</title>
    {% endblock %}
</head>
<body>
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
        &copy; Copyright 2008 by <a href="http://domain.invalid/">you</a>.
        {% endblock %}
    </div>
</body>
</html>
```

在这个示例中，`{% block %}` 标签定义了四个块，子模板可以填充它们。`block` 标签所做的只是告诉模板引擎，子模板可以覆盖模板中的这些占位符。

`block` 标签可以位于其他块（如 `if`）内部，但无论 `if` 块是否实际渲染，它们都会始终被执行。

### 子模板

子模板可能如下所示：

```jinja
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style type="text/css">
        .important { color: #336699; }
    </style>
{% endblock %}
{% block content %}
    <h1>Index</h1>
    <p class="important">
      Welcome to my awesome homepage.
    </p>
{% endblock %}
```

`{% extends %}` 标签是关键。它告诉模板引擎，此模板“扩展”另一个模板。当模板系统求值此模板时，它首先定位父模板。extends 标签应该是模板中的第一个标签。它之前的所有内容都会正常打印出来，并可能造成混淆。关于此行为的详细信息以及如何利用它，请参见[空默认回退]。另外，无论周围条件求值为真还是假，块都会始终被填充。

模板的文件名取决于模板加载器。例如，[FileSystemLoader] 允许你通过给出文件名来访问其他模板。你可以使用斜杠访问子目录中的模板：

```jinja
{% extends "layout/default.html" %}
```

但此行为可能取决于嵌入 Jinja 的应用程序。注意，由于子模板没有定义 `footer` 块，因此会使用父模板中的值。

你不能在同一个模板中定义多个同名 `{% block %}` 标签。存在此限制是因为块标签在“两个”方向上工作。也就是说，块标签不仅提供要填充的占位符，还定义了在*父模板*中填充该占位符的内容。如果模板中有两个同名 `{% block %}` 标签，该模板的父模板就不知道该使用哪个块的内容。

不过，如果你想多次打印一个块，可以使用特殊的 `self` 变量并按该名称调用块：

```jinja
<title>{% block title %}{% endblock %}</title>
<h1>{{ self.title() }}</h1>
{% block body %}{% endblock %}
```

### 超级块

可以通过调用 `super()` 来渲染父块的内容。这会返回父块的结果：

```jinja
{% block sidebar %}
    <h3>Table Of Contents</h3>
    ...
    {{ super() }}
{% endblock %}
```

### 嵌套 extends

在多层 `{% extends %}` 的情况下，`super` 引用可以链式调用（如 `super.super()`），以跳过继承树中的层级。

例如：

```jinja
# parent.tmpl
body: {% block body %}Hi from parent.{% endblock %}

# child.tmpl
{% extends "parent.tmpl" %}
{% block body %}Hi from child. {{ super() }}{% endblock %}

# grandchild1.tmpl
{% extends "child.tmpl" %}
{% block body %}Hi from grandchild1.{% endblock %}

# grandchild2.tmpl
{% extends "child.tmpl" %}
{% block body %}Hi from grandchild2. {{ super.super() }} {% endblock %}
```

渲染 `child.tmpl` 将得到 `body: Hi from child. Hi from parent.`

渲染 `grandchild1.tmpl` 将得到 `body: Hi from grandchild1.`

渲染 `grandchild2.tmpl` 将得到 `body: Hi from grandchild2. Hi from parent.`

### 命名块结束标签

Jinja 允许在结束标签后放置块名称，以提高可读性：

```jinja
{% block sidebar %}
    {% block inner_sidebar %}
        ...
    {% endblock inner_sidebar %}
{% endblock sidebar %}
```

但是，`endblock` 单词后面的名称必须与块名称匹配。

### 块嵌套与作用域

块可以嵌套以实现更复杂的布局。默认情况下，块不能访问块外部（外部作用域）的变量：

```jinja
{% for item in seq %}
    <li>{% block loop_item %}{{ item }}{% endblock %}</li>
{% endfor %}
```

此示例将输出空的 `<li>` 项，因为 `item` 在块内不可用。原因是，如果块被子模板替换，就会出现一个未在块中定义或未传递给上下文的变量。

从 Jinja 2.2 开始，你可以通过向块声明添加 `scoped` 修饰符，将块设置为“scoped”，从而显式指定变量在块中可用：

```jinja
{% for item in seq %}
    <li>{% block loop_item scoped %}{{ item }}{% endblock %}</li>
{% endfor %}
```

覆盖块时，不必提供 `scoped` 修饰符。

### 必需块

块可以标记为 `required`。它们必须在某个时刻被覆盖，但不一定由直接子模板覆盖。必需块只能包含空格和注释，并且不能直接渲染。

`page.txt`：

```jinja
{% block body required %}{% endblock %}
```

`issue.txt`：

```jinja
{% extends "page.txt" %}
```

`bug_report.txt`：

```jinja
{% extends "issue.txt" %}
{% block body %}Provide steps to demonstrate the bug.{% endblock %}
```

渲染 `page.txt` 或 `issue.txt` 将引发 `TemplateRuntimeError`，因为它们没有覆盖 `body` 块。渲染 `bug_report.txt` 将成功，因为它确实覆盖了该块。

当与 `scoped` 组合时，`required` 修饰符必须放在 scoped 修饰符*之后*。以下是一些有效示例：

```jinja
{% block body scoped %}{% endblock %}
{% block body required %}{% endblock %}
{% block body scoped required %}{% endblock %}
```

### 模板对象

`extends`、`include` 和 `import` 可以接受模板对象，而不是要加载的模板名称。这在某些高级情况下可能很有用，因为你可以先用 Python 代码加载模板，然后将其传入 `render`。

```py
if debug_mode:
    layout = env.get_template("debug_layout.html")
else:
    layout = env.get_template("layout.html")

user_detail = env.get_template("user/detail.html")
return user_detail.render(layout=layout)
```

```jinja
{% extends layout %}
```

注意，`extends` 接收的是传递给 `render` 的模板对象变量，而不是字符串。

## HTML 转义

从模板生成 HTML 时，变量总是有可能包含影响结果 HTML 的字符。有两种方法：

1. 手动转义每个变量；或
2. 默认自动转义所有内容。

Jinja 支持这两种方式。使用哪种取决于应用程序配置。默认配置是不自动转义；原因有多种：

- 转义除安全值之外的所有内容也意味着 Jinja 会转义已知不包含 HTML 的变量（例如数字、布尔值），这可能会造成巨大的性能损失。
- 关于变量安全性的信息非常脆弱。强制转换安全值和不安全值时，返回值可能会被双重转义的 HTML。

### 使用手动转义

如果启用了手动转义，则**你**有责任在需要时转义变量。要转义什么？如果你有一个*可能*包含以下任何字符（`>`、`<`、`&` 或 `"`）的变量，**应该**转义它，除非该变量包含格式良好且可信的 HTML。转义的方法是将变量通过 `|e` 过滤器：

```jinja
{{ user.username|e }}
```

### 使用自动转义

启用自动转义时，默认情况下所有内容都会被转义，除非值被显式标记为安全。变量和表达式可以通过以下方式标记为安全：

1. 应用程序在上下文字典中使用 `markupsafe.Markup` 标记；
2. 在模板中使用 `|safe` 过滤器。

如果你标记为安全的字符串经过其他不理解该标记的 Python 代码，该标记可能会丢失。要注意数据何时被标记为安全，以及在到达模板之前是如何处理的。

如果一个值已经被转义但未标记为安全，自动转义仍会发生，并导致字符被双重转义。如果你知道数据已经安全但未标记，请确保将其包装在 `Markup` 中或使用 `|safe` 过滤器。

Jinja 函数（宏、`super`、`self.BLOCKNAME`）始终返回标记为安全的模板数据。

在启用自动转义的模板中，字符串字面量被视为不安全，因为原生 Python 字符串不安全。