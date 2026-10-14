https://freemarker.apache.org/docs/index.html
[github](https://github.com/apache/freemarker)

页眉导航
- [索引](https://freemarker.apache.org/docs/alphaidx.html)
- [`?内置函数`](https://freemarker.apache.org/docs/ref_builtins_alphaidx.html)
- [`#指令`](https://freemarker.apache.org/docs/ref_directive_alphaidx.html)
- [`.特殊变量`](https://freemarker.apache.org/docs/ref_specvar.html)

## Template Language Reference

https://freemarker.apache.org/docs/ref.html

### Directive Reference

https://freemarker.apache.org/docs/ref_directives.html

#### Alphabetical index —— 指令索引

https://freemarker.apache.org/docs/ref_directive_alphaidx.html

##### User-defined directive `<@...>` —— 用户定义指令

https://freemarker.apache.org/docs/ref_directive_userDefined.html#ref.directive.userDefined

```
<@user_def_dir_exp param1=val1 param2=val2 ... paramN=valN/>
```
(Note the XML-style `/` before the `>`)

##### assign —— 赋值

```
<#assign name1=value1 name2=value2 ... nameN=valueN>
or
<#assign same as above... in namespacehash>
or
<#assign name>
  capture this
</#assign>
or
<#assign name in namespacehash>
  capture this
</#assign>
```

##### list, else, items, sep, break, continue —— 循环结构

```
<#list sequence as item>
    Part repeated for each item
</#list>

<#list hash as key, value>
    Part repeated for each key-value pair
</#list>
```

### Built-in Reference

https://freemarker.apache.org/docs/ref_builtins.html

#### Built-ins for strings —— 字符串函数

https://freemarker.apache.org/docs/ref_builtins_string.html

##### url —— url 编码

```
<#assign x = 'a/b c'>
${x?url}
```

##### j_string —— java 转义

##### js_string —— JavaScript 转义

#### Built-ins for numbers —— 数字函数

https://freemarker.apache.org/docs/ref_builtins_number.html

##### lower_abc —— 数字转为小写字母

Converts `1`, `2`, `3`, etc., to the string `"a"`, `"b"`, `"c"`, etc. 

When reaching `"z"`, it continues like `"aa"`, `"ab"`, etc.

```
<#list 1..30 as n>${n?lower_abc} </#list>
```

```log
a b c d e f g h i j k l m n o p q r s t u v w x y z aa ab ac ad 
```

#### Built-ins for hashes —— 字典函数

https://freemarker.apache.org/docs/ref_builtins_hash.html

##### keys —— 包含字典中所有查找键的序列

```
<#list .data_model?keys as key>
    ${key}
</#list>
```

##### values —— 包含字典中所有变量（键值对中的值）的序列

```
<#list .data_model?values as value>
    ${value}
</#list>
```

#### Seldom used and expert built-ins —— 少见的高阶函数

https://freemarker.apache.org/docs/ref_builtins_expert.html

##### 🥷 eval —— 输入表达式字符串，解析为表达式执行

此内置函数将字符串作为 `FTL 表达式` 进行评估。例如，`"1+2"？eval` 会返回数字 3。（若要渲染存储在字符串中的模板，请使用 [interpret 内置函数]。）

> 无括号执行

```
${'"freemarker.template.utility.Execute"?new()("id")'?eval}
```

##### 🥷 interpret —— 输入模板字符串，解析为模板后设置用户指令

此内置函数将字符串解析为 FTL 模板，并返回一个用户自定义的指令，该指令会执行该模板，就像在当前位置包含了一个具有相同内容的模板一样。

> 无括号执行

```
<#assign templateSource = '${"freemarker.template.utility.Execute"?new()("id")}'>
<#assign inlineTemplate = templateSource?interpret>
<@inlineTemplate />
```
1. 准备模板字符串
2. 设置模板为用户指令
3. 执行用户指令

##### ⚔️ new —— 输入类完全限定名字符串，得到构造函数

用于创建某个 `TemplateModel` 实现类的变量。

在 `?` 的左侧指定一个字符串，即某个 `TemplateModel` 实现类的完全限定类名。其结果是一个方法变量，用于调用构造函数并返回新变量。

> freemarker 模板注入核心，`构造函数 = "完全限定类名字符串"?new()`

示例：

```freemarker
<#-- 通过调用该类的无参构造函数创建用户自定义指令 -->
<#assign word_wrapp = "com.acmee.freemarker.WordWrapperDirective"?new()>
<#-- 通过调用带一个数值参数的构造函数创建用户自定义指令 -->
<#assign word_wrapp_narrow = "com.acmee.freemarker.WordWrapperDirective"?new(40)>
```

有关构造函数参数如何解包以及如何选择重载构造函数的更多信息，请阅读：[程序员指南/杂项/Bean 包装器]

此内建项可能存在安全隐患，因为模板作者可以创建任意 Java 对象，并在这些对象实现 `TemplateModel` 时使用它们。此外，模板作者还可以触发甚至未实现 `TemplateModel` 的类的静态初始化。自 2.3.17 起，你可以使用 `Configuration.setNewBuiltinClassResolver(TemplateClassResolver)` 或 `new_builtin_class_resolver` 设置来限制可通过此内建项访问的类。更多信息请参阅 Java API 文档。如果你允许不太可信的用户上传模板，则务必研究此主题。

###### `?new()` 源码追踪

https://github.com/apache/freemarker/blob/e156e5faf9325e7ec05b781411bbf331aff98dfc/freemarker-core/src/main/java/freemarker/core/NewBI.java

```java
/**
 * A built-in that allows us to instantiate an instance of a java class.
 * Usage is something like: <code>&lt;#assign foobar = "foo.bar.MyClass"?new()></code>;
 */
class NewBI extends BuiltIn {
    
    ...

    class ConstructorFunction implements TemplateMethodModelEx {

        private final Class<?> cl;
        private final Environment env;
        
        public ConstructorFunction(String classname, Environment env, Template template) throws TemplateException {
            this.env = env;
            cl = env.getNewBuiltinClassResolver().resolve(classname, env, template);
            ...
        }

        ...
    }
}
```
- 追踪 `resolve()`

https://github.com/apache/freemarker/blob/2.3-gae/freemarker-core/src/main/java/freemarker/core/OptInTemplateClassResolver.java#L104

```java
/**
 * A {@link TemplateClassResolver} that resolves only the classes whose name was specified in the constructor.
 */
public class OptInTemplateClassResolver implements TemplateClassResolver {

    ...
    @Override
    public Class resolve(String className, Environment env, Template template)
            throws TemplateException {
        ...
            } else {
                try {
                    return ClassUtil.forName(className);
                } catch (ClassNotFoundException e) {
                    throw new _MiscTemplateException(e, env);
                }
            }
        }
    }
    ...
}
```
- 追踪 `forName()`


https://github.com/apache/freemarker/blob/2.3-gae/freemarker-core/src/main/java/freemarker/template/utility/ClassUtil.java#L79


```java
/**
 */
public class ClassUtil {
    private ClassUtil() {
    }
    
    /**
     * Similar to {@link Class#forName(java.lang.String)}, but attempts to load
     * through the thread context class loader. Only if thread context class
     * loader is inaccessible, or it can't find the class will it attempt to
     * fall back to the class loader that loads the FreeMarker classes.
     */
    public static Class forName(String className)
    throws ClassNotFoundException {
        try {
            ClassLoader ctcl = Thread.currentThread().getContextClassLoader();
            if (ctcl != null) {  // not null: we don't want to fall back to the bootstrap class loader
                return Class.forName(className, true, ctcl);
            }
        } catch (ClassNotFoundException e) {
            ;// Intentionally ignored
        } catch (SecurityException e) {
            ;// Intentionally ignored
        }
        // Fall back to the defining class loader of the FreeMarker classes 
        return Class.forName(className);
    }
    ...
}
```

### Special Variable Reference —— 内置变量

https://freemarker.apache.org/docs/ref_specvar.html

特殊变量是由 FreeMarker 引擎自身定义的变量。要访问它们，使用 `.variable_name` 的语法。例如，不能简单地写 `version`；应当写为 `.version`。

- `version`
    返回版本号

- `vars`
    变量字典。不支持 `?keys` and `?values`

- `namespace`
    当前命名空间字典。不含 `data-model`

- `main`
    主命名空间字典。不含 `data-model`

- `data_model`
    `data_model`字典 不含 `global`

- `now`
    返回当前日期

打印字典
```
<#list .data_model as key, value>
    ${key}: ${value}
</#list>
```

## Template Author's GuideThe 

https://freemarker.apache.org/docs/dgui.html

### Template

https://freemarker.apache.org/docs/dgui_template.html

#### Interpolations —— 插值

https://freemarker.apache.org/docs/dgui_template_valueinsertion.html

插值的格式为 `${expression}`，其中 `expression` 可以是各种表达式（例如 `${100 + x}`）。

#### Expressions —— 表达式

https://freemarker.apache.org/docs/dgui_template_exp.html

当为插值或指令参数提供值时，可以使用变量或更复杂的表达式。例如，如果 `x` 是数字 8，`y` 是 5，则 `(x + y)/2` 的值为数值 6.5。

在深入探讨细节之前，先看一些具体的示例：

- 为插值提供值时：
  插值的使用方式为 `${expression}`，其中 `expression` 给出要作为文本插入到输出中的值。因此，`${(5 + 8)/2}` 会在输出中打印 "6.5"（如果输出语言不是美式英语，则可能是 "6,5"）。

- 为指令参数提供值时：
  在“入门”部分中，您已经见过 `if` 指令。该指令的语法为：`<#if expression>...</#if>`。此处的表达式必须计算为布尔值。例如，在 `<#if 2 < 3>` 中，`2 < 3`（2 小于 3）是一个计算结果为 `true` 的表达式。

### 快速概览（速查表）

对于已经了解 FreeMarker 或经验丰富的程序员，以下是一个提醒：

- 直接指定值
  - 字符串：`"Foo"` 或 `'Foo'` 或 `"It's \"quoted\""` 或 `'It\'s "quoted"'` 或 `r"C:\raw\string"`
  - 数字：`123.45`
  - 布尔值：`true`、`false`
  - 序列：`["foo", "bar", 123.45]`；范围：`0..9`、`0..<10`（或 `0..!10`）、`0..`
  - 哈希：`{"name":"green mouse", "price":150}`
- 检索变量
  - 顶层变量：`user`
  - 从哈希中检索数据：`user.name`、`user["name"]`
  - 从序列中检索数据：`products[5]`
  - 特殊变量：`.main`
- 字符串操作
  - 插值与拼接：`"Hello ${user}!"`（或 `"Hello " + user + "!"`）
  - 获取字符：`name[0]`
  - 字符串切片：包含结束位置：`name[0..4]`，排除结束位置：`name[0..<5]`，基于长度（宽松）：`name[0..*5]`，移除开头：`name[5..]`
- 序列操作
  - 拼接：`users + ["guest"]`
  - 序列切片：包含结束位置：`products[20..29]`，排除结束位置：`products[20..<30]`，基于长度（宽松）：`products[20..*10]`，移除开头：`products[20..]`
- 哈希操作
  - 拼接：`passwords + { "joe": "secret42" }`
- 算术计算：`(x * 1.5 + 10) / 2 - y % 100`
- 比较：`x == y`、`x != y`、`x < y`、`x > y`、`x >= y`、`x <= y`、`x lt y`、`x lte y`、`x gt y`、`x gte y` 等
- 逻辑运算：`!registered && (firstVisit || fromEurope)`
- 内建函数：`name?upper_case`、`path?ensure_starts_with('/')`
- 方法调用：`repeat("What", 3)`
- 缺失值处理运算符
  - 默认值：`name!"unknown"` 或 `(user.name)!"unknown"` 或 `name!` 或 `(user.name)!`
  - 缺失值测试：`name??` 或 `(user.name)??`
- 赋值运算符：`=`、`+=`、`-=`、`*=`、`/=`、`%=`、`++`、`--`
- 局部 Lambda 表达式：`x -> x + 1`、`(x, y) -> x + y`

另见：运算符优先级

### 直接指定值

通常，您希望直接指定一个值，而不是作为某些计算的结果。

#### 字符串

要直接指定字符串值，请将文本放在双引号中，例如：`"some text"`，或者放在单引号中，例如：`'some text'`。这两种形式是等价的。如果文本本身包含用于引用的字符（`"` 或 `'`）或反斜杠，则必须在它们前面加上反斜杠；这称为转义。您可以直接在文本中输入任何其他字符，包括[换行符]。

**模板**
```freemarker
${"It's \"quoted\" and
this is a backslash: \\"}

${'It\'s "quoted" and
this is a backslash: \\'}
```

**输出**
```text
It's "quoted" and
this is a backslash: \
It's "quoted" and
this is a backslash: \
```

以下是所有支持的转义序列列表。在字符串字面量中所有其他反斜杠的用法都是错误的，任何尝试使用该模板的操作都将失败。

- `\"`
  双引号 (u0022)
- `\'`
  单引号 (u0027)
- `\{`
  左大括号：`{`
- `\=`
  等号：`=`（FreeMarker 2.3.28 起支持）
- `\\`
  反斜杠 (u005C)
- `\n`
  换行符 (u000A)
- `\r`
  回车符 (u000D)
- `\t`
  水平制表符 (u0009)
- `\b`
  退格符 (u0008)
- `\f`
  换页符 (u000C)
- `\l`
  小于号：`<`
- `\g`
  大于号：`>`
- `\a`
  和号：`&`
- `\xCode` 🥷
  具有十六进制 Unicode 代码（UCS 代码）的字符

`\x` 后面的 `Code` 是 1 到 4 位十六进制数字。例如，以下写法都会在字符串中放入版权符号：`"\xA9 1999-2001"`、`"\x0A9 1999-2001"`、`"\x00A9 1999-2001"`。当最后一个十六进制数字直接后面的字符可以被解释为十六进制数字时，您必须使用完整的 4 位数字，否则 FreeMarker 会误解您的意思。

请注意，字符序列 `${` 和 `#{`（根据配置的语法，偶尔也可能是 `[=`）具有特殊含义。它们用于插入表达式的值（通常是变量的值，如 `"Hello ${user}!"`）。这将在后文解释。如果您想打印 `${` 或 `#{`（或 `[=`），您应该使用下文解释的原始字符串字面量，或者转义 `{`，如 `"foo $\{bar}"`（或者转义 `=`，如 `"foo [\=bar]"`）。

一种特殊的字符串字面量是原始字符串字面量。在原始字符串字面量中，反斜杠和 `${` 没有特殊含义，它们被视为普通字符。要指示字符串字面量是原始字符串字面量，您必须在开头的双引号或单引号前直接放置一个 `r`（`r"原始字符串"`）。

**模板**
```
${r"${foo}"}
${r"C:\foo\bar"}
```

**输出**
```text
${foo}
C:\foo\bar
```