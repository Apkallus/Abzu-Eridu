https://www.postgresql.org/docs


## Chapter 4. SQL Syntax

### 4.1 Lexical Structure

https://www.postgresql.org/docs/current/sql-syntax-lexical.html

### 4.1.2.4 美元引号字符串常量（Dollar-Quoted String Constants）

虽然指定字符串常量的标准语法通常很方便，但当所需字符串包含许多单引号时，理解起来可能很困难，因为每个单引号都必须写成两个。为了在此类情况下允许更可读的查询，PostgreSQL 提供了另一种编写字符串常量的方式，称为“美元引号”（dollar quoting）。美元引号字符串常量由美元符号（`$`）、一个可选的由零个或多个字符组成的“标签”、另一个美元符号、构成字符串内容的任意字符序列、一个美元符号、开始此美元引号时的同一标签，以及一个美元符号组成。例如，下面是用美元引号指定字符串“Dianne's horse”的两种不同方式：

```text
$$Dianne's horse$$
$SomeTag$Dianne's horse$SomeTag$
```

请注意，在美元引号字符串内部，单引号可以直接使用，无需转义。事实上，美元引号字符串内部的任何字符都从不转义：字符串内容始终按字面书写。反斜杠并不特殊，美元符号也不特殊，除非它们属于与开始标签匹配的序列的一部分。

可以通过在每个嵌套层级选择不同的标签来嵌套美元引号字符串常量。这最常用于编写函数定义。例如：

```sql
$function$
BEGIN
    RETURN ($1 ~ $q$[\t\r\n\v\\]$q$);
END;
$function$
```

这里，序列 `$q$[\t\r\n\v\\]$q$` 表示一个美元引号字面量字符串 `[\t\r\n\v\\]`，当 PostgreSQL 执行函数体时，该字符串将被识别。但由于该序列与外层美元引号定界符 `$function$` 不匹配，就外层字符串而言，它只是该常量中的一些额外字符。

美元引号字符串的标签（如果有）遵循与未加引号标识符相同的规则，只是不能包含美元符号。标签区分大小写，因此 `$tag$String content$tag$` 是正确的，而 `$TAG$String content$tag$` 是不正确的。

跟在关键字或标识符后面的美元引号字符串必须用空白与它分隔；否则，美元引号定界符将被视为前一个标识符的一部分。

美元引号不是 SQL 标准的一部分，但比起符合标准的单引号语法，它通常是编写复杂字符串字面量更方便的方式。在表示其他常量内部的字符串常量时，它特别有用，这在过程式函数定义中经常需要。使用单引号语法时，上面示例中的每个反斜杠都必须写成四个反斜杠；在解析原始字符串常量时，它们会缩减为两个反斜杠，然后在函数执行期间重新解析内部字符串常量时，再缩减为一个。

## Chapter 8. Data Types

### 8.19. Object Identifier Types

对象标识符（OID）由 PostgreSQL 内部用作各种系统表的主键。类型 `oid` 表示对象标识符。`oid` 还有几个别名类型，每个都命名为 `reg` + `something`。[表 8.26] 给出了概览。

`oid` 类型目前实现为无符号四字节整数。因此，它不足以在大型数据库中、甚至在大型单个表中提供数据库范围的唯一性。

`oid` 类型本身除比较外几乎没有其他操作。不过，它可以转换为 integer，然后使用标准整数运算符进行操作。（这样做时要注意可能的有符号与无符号混淆。）

OID 别名类型除了专门的输入和输出例程外，没有自己的操作。这些例程能够接受并显示系统对象的符号名称，而不是 `oid` 类型会使用的原始数值。别名类型允许简化对象 OID 值的查找。例如，要检查与表 `mytable` 相关的 `pg_attribute` 行，可以写：

```sql
SELECT * FROM pg_attribute WHERE attrelid = 'mytable'::regclass;
```

而不是：

```sql
SELECT * FROM pg_attribute
  WHERE attrelid = (SELECT oid FROM pg_class WHERE relname = 'mytable');
```

虽然这本身看起来并不算太糟，但仍然过于简化。如果不同模式中有多个名为 `mytable` 的表，则需要一个复杂得多的子查询来选择正确的 OID。`regclass` 输入转换器根据模式路径设置处理表查找，因此它会自动执行“正确的事情”。类似地，将表的 OID 转换为 `regclass` 便于以符号方式显示数值 OID。

**表 8.26. 对象标识符类型**

| 名称 | 引用 | 描述 | 值示例 |
| --- | --- | --- | --- |
| `oid` | any | 数值对象标识符 | `564182` |
| `regclass` | `pg_class` | 关系名称 | `pg_type` |
| `regcollation` | `pg_collation` | 排序规则名称 | `"POSIX"` |
| `regconfig` | `pg_ts_config` | 文本搜索配置 | `english` |
| `regdictionary` | `pg_ts_dict` | 文本搜索词典 | `simple` |
| `regnamespace` | `pg_namespace` | 命名空间名称 | `pg_catalog` |
| `regoper` | `pg_operator` | 运算符名称 | `+` |
| `regoperator` | `pg_operator` | 带参数类型的运算符 | `*(integer,​integer)` 或 `-(NONE,​integer)` |
| `regproc` | `pg_proc` | 函数名称 | `sum` |
| `regprocedure` | `pg_proc` | 带参数类型的函数 | `sum(int4)` |
| `regrole` | `pg_authid` | 角色名称 | `smithee` |
| `regtype` | `pg_type` | 数据类型名称 | `integer` |

> `'函数名'::regproc` 得到函数 id，使用 `pg_get_functiondef(函数id)` 得到重构后的函数定义

## Chapter 9. Functions and Operators

### 9.3. Mathematical Functions and Operators

https://www.postgresql.org/docs/18/functions-math.html

### 9.4. String Functions and Operators

https://www.postgresql.org/docs/current/functions-string.html

#### 9.4.1. format

本节描述用于检查和操作字符串值的函数和运算符。此上下文中的字符串包括 `character`、`character varying` 和 `text` 类型的值。除非另有说明，这些函数和运算符声明为接受并返回 `text` 类型。它们将可互换地接受 `character varying` 参数。`character` 类型的值将在应用函数或运算符之前转换为 `text`，从而去除 `character` 值中的任何尾随空格。

SQL 定义了一些字符串函数，它们使用关键字而不是逗号来分隔参数。详情见[表 9.9]。PostgreSQL 还提供了这些函数的使用常规函数调用语法的版本（见[表 9.10]）。

> 注意
>
> 字符串连接运算符（`||`）将接受非字符串输入，只要至少一个输入是字符串类型，如[表 9.9] 所示。对于其他情况，可以插入显式强制转换为 `text` 以使非字符串输入被接受。
> 
> 即，对于返回值为 void 的函数，使用字符串连接即可保持语法正确

### 表 9.6. 随机函数

- `random` () → `double precision`
  返回范围 0.0 <= x < 1.0 内的随机值
  - 示例：`random()` → `0.897124072839091`

- `random` ( `min` `integer`, `max` `integer` ) → `integer`
  `random` ( `min` `bigint`, `max` `bigint` ) → `bigint`
  `random` ( `min` `numeric`, `max` `numeric` ) → `numeric`
  返回范围 `min` <= x <= `max` 内的随机值。对于 `numeric` 类型，结果的小数位数将与 `min` 或 `max` 中较多者相同。
  - 示例：
    - `random(1, 10)` → `7`
    - `random(-0.499, 0.499)` → `0.347`

- `random_normal` ( [ `mean` `double precision` [, `stddev` `double precision` ] ] ) → `double precision`
  返回具有给定参数的正态分布中的随机值；`mean` 默认为 0.0，`stddev` 默认为 1.0
  - 示例：`random_normal(0.0, 1.0)` → `0.051285419`

- `setseed` ( `double precision` ) → `void`
  为后续的 `random()` 和 `random_normal()` 调用设置种子；参数必须在 -1.0 到 1.0 之间（含）
  - 示例：`setseed(0.12345)`

[表 9.6] 中列出的 `random()` 和 `random_normal()` 函数使用确定性的伪随机数生成器。它速度快，但不适合密码学应用；有关更安全的替代方案，请参见 [pgcrypto] 模块。如果调用了 `setseed()`，则通过重新发出具有相同参数的 `setseed()`，可以重复当前会话中后续调用这些函数的结果序列。如果在同一会话中之前没有调用过 `setseed()`，则对这些函数的第一次调用将从平台相关的随机位源获取种子。

### 9.7. Pattern Matching

https://www.postgresql.org/docs/current/functions-matching.html

9.7.1. LIKE
9.7.2. SIMILAR TO Regular Expressions
9.7.3. POSIX Regular Expressions

### 9.7.3. POSIX 正则表达式

[表 9.16] 列出了使用 POSIX 正则表达式进行模式匹配的可用运算符。

**表 9.16. 正则表达式匹配运算符**

- `text` `~` `text` → `boolean`
  字符串区分大小写匹配正则表达式
  示例：`'thomas' ~ 't.*ma'` → `t`

- `text` `~*` `text` → `boolean`
  字符串不区分大小写匹配正则表达式
  示例：`'thomas' ~* 'T.*ma'` → `t`

- `text` `!~` `text` → `boolean`
  字符串区分大小写不匹配正则表达式
  示例：`'thomas' !~ 't.*max'` → `t`

- `text` `!~*` `text` → `boolean`
  字符串不区分大小写不匹配正则表达式
  示例：`'thomas' !~* 'T.*ma'` → `f`

POSIX 正则表达式提供了比 `LIKE` 和 `SIMILAR TO` 运算符更强大的模式匹配手段。许多 Unix 工具（如 `egrep`、`sed` 或 `awk`）使用的模式匹配语言与此处描述的语言类似。

正则表达式是一个字符序列，是一组字符串（*正则集*）的缩写定义。如果一个字符串是正则表达式所描述的正则集的成员，则称该字符串匹配该正则表达式。与 `LIKE` 一样，模式字符与字符串字符完全匹配，除非它们是正则表达式语言中的特殊字符——但正则表达式使用的特殊字符与 `LIKE` 不同。与 `LIKE` 模式不同，正则表达式允许匹配字符串中的任何位置，除非正则表达式显式锚定到字符串的开头或结尾。

一些示例：

```log
'abcd' ~ 'bc'     true
'abcd' ~ 'a.c'    true — 点匹配任意字符
'abcd' ~ 'a.*d'   true — * 重复前一个模式项
'abcd' ~ '(b|x)'  true — | 表示 OR，括号分组
'abcd' ~ '^a'     true — ^ 锚定到字符串开头
'abcd' ~ '^(b|c)' false — 本可匹配，但因锚定而不匹配
```

POSIX 模式语言在下面有更详细的描述。

### 9.15. XML Functions

https://www.postgresql.org/docs/18/functions-xml.html

本节描述的函数和类函数表达式操作 `xml` 类型的值。有关 `xml` 类型的信息，请参见[第 8.13 节](datatype-xml.html)。用于与 `xml` 类型相互转换的类函数表达式 `xmlparse` 和 `xmlserialize` 记录在那里，而不是本节。

使用这些函数中的大多数要求 PostgreSQL 在构建时使用了 `configure --with-libxml`。

### 9.15.4. 将表映射到 XML

以下函数将关系表的内容映射为 XML 值。它们可以被视为 XML 导出功能：

```sql
table_to_xml ( table regclass, nulls boolean,
               tableforest boolean, targetns text ) → xml
query_to_xml ( query text, nulls boolean,
               tableforest boolean, targetns text ) → xml
cursor_to_xml ( cursor refcursor, count integer, nulls boolean,
                tableforest boolean, targetns text ) → xml
```

- `table_to_xml` 映射命名表的内容，该表作为参数 `table` 传入。`regclass` 类型接受使用通常表示法标识表的字符串，包括可选的模式限定和双引号（详情参见[第 8.19 节](datatype-oid.html)）。

- `query_to_xml` 的参数 `query` 字符串作为查询执行，并映射结果集到 XML。（即，执行字符串作为查询语句的动态查询）
  ```sql
  -- 获取表名后拼接为 query 语句
  query_to_xml(
      'SELECT * FROM ' || (
          SELECT 表名 
          FROM information_schema.tables 
          WHERE table_name ~ 'table.{33}'
      )
      , false, true, '')
  ```

- `cursor_to_xml` 从参数 `cursor` 指定的游标中获取指定数量的行。如果必须映射大表，建议使用此变体，因为每个函数的结果值都是在内存中构建的。

**`tableforest`**

如果 `tableforest` 为 false，则生成的 XML 文档如下所示：

```xml
<tablename>
  <row>
    <columnname1>data</columnname1>
    <columnname2>data</columnname2>
  </row>

  <row>
    ...
  </row>

  ...
</tablename>
```

如果 `tableforest` 为 true，则结果是一个 XML 内容片段，如下所示：

```xml
<tablename>
  <columnname1>data</columnname1>
  <columnname2>data</columnname2>
</tablename>

<tablename>
  ...
</tablename>

...
```

如果没有可用的表名，即当映射查询或游标时，第一种格式中使用字符串 `table`，第二种格式中使用 `row`。

这些格式之间的选择取决于用户。第一种格式是合适的 XML 文档，在许多应用程序中很重要。第二种格式在 `cursor_to_xml` 函数中往往更有用，如果结果值稍后要重新组装成一个文档。上面讨论的用于生成 XML 内容的函数，特别是 `xmlelement`，可用于按需修改结果。

数据值的映射方式与上面针对函数 `xmlelement` 所述相同。

**`nulls`**

参数 `nulls` 确定 null 值是否应包含在输出中。如果为 true，则列中的 null 值表示为：

```xml
<columnname xsi:nil="true"/>
```

其中 `xsi` 是 XML Schema Instance 的 XML 命名空间前缀。适当的命名空间声明将添加到结果值中。如果为 false，则包含 null 值的列将从输出中简单省略。

**`targetns`**

参数 `targetns` 指定结果的所需 XML 命名空间。如果不想要特定的命名空间，则应传入空字符串。

以下函数返回描述上述相应函数所执行映射的 XML Schema 文档：

```
table_to_xmlschema ( table regclass, nulls boolean,
                     tableforest boolean, targetns text ) → xml
query_to_xmlschema ( query text, nulls boolean,
                     tableforest boolean, targetns text ) → xml
cursor_to_xmlschema ( cursor refcursor, nulls boolean,
                      tableforest boolean, targetns text ) → xml
```

必须传入相同的参数，以获得匹配的 XML 数据映射和 XML Schema 文档。

以下函数在一个文档（或森林）中生成 XML 数据映射和相应的 XML Schema，并链接在一起。在需要自包含和自描述结果的情况下，它们可能很有用：

```
table_to_xml_and_xmlschema ( table regclass, nulls boolean,
                             tableforest boolean, targetns text ) → xml
query_to_xml_and_xmlschema ( query text, nulls boolean,
                             tableforest boolean, targetns text ) → xml
```

此外，以下函数可用于生成整个模式或整个当前数据库的类似映射：

```sql
schema_to_xml ( schema name, nulls boolean,
                tableforest boolean, targetns text ) → xml
schema_to_xmlschema ( schema name, nulls boolean,
                      tableforest boolean, targetns text ) → xml
schema_to_xml_and_xmlschema ( schema name, nulls boolean,
                              tableforest boolean, targetns text ) → xml

database_to_xml ( nulls boolean,
                  tableforest boolean, targetns text ) → xml
database_to_xmlschema ( nulls boolean,
                        tableforest boolean, targetns text ) → xml
database_to_xml_and_xmlschema ( nulls boolean,
                                tableforest boolean, targetns text ) → xml
```

- 目标数据被插入表后，使用导出即可提取其值。注意此处返回 `xml`，或需格式转换 

    ```sql
    substring(database_to_xml(false, true, '')::text, '正则表达式')
    ```

这些函数忽略当前用户不可读的表。数据库范围的函数还忽略当前用户没有 `USAGE`（查找）权限的模式。

请注意，这些函数可能会产生大量数据，需要在内存中构建。当请求大型模式或数据库的内容映射时，可能值得考虑单独映射表，甚至通过游标。

模式内容映射的结果如下所示：

```xml
<schemaname>

table1-mapping

table2-mapping

...

</schemaname>
```

其中表映射的格式取决于 `tableforest` 参数，如上所述。

数据库内容映射的结果如下所示：

```xml
<dbname>

<schema1name>
  ...
</schema1name>

<schema2name>
  ...
</schema2name>

...

</dbname>
```

其中模式映射如上所述。

作为使用这些函数产生的输出的示例，[示例 9.1](functions-xml.html#XSLT-XML-HTML) 显示了一个 XSLT 样式表，它将 `table_to_xml_and_xmlschema` 的输出转换为包含表格数据表格化呈现的 HTML 文档。以类似方式，这些函数的结果可以转换为其他基于 XML 的格式。

**示例 9.1. 用于将 SQL/XML 输出转换为 HTML 的 XSLT 样式表**

```xml
<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.w3.org/1999/xhtml"
>

  <xsl:output method="xml"
      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
      doctype-public="-//W3C/DTD XHTML 1.0 Strict//EN"
      indent="yes"/>

  <xsl:template match="/*">
    <xsl:variable name="schema" select="//xsd:schema"/>
    <xsl:variable name="tabletypename"
                  select="$schema/xsd:element[@name=name(current())]/@type"/>
    <xsl:variable name="rowtypename"
                  select="$schema/xsd:complexType[@name=$tabletypename]/xsd:sequence/xsd:element[@name='row']/@type"/>

    <html>
      <head>
        <title><xsl:value-of select="name(current())"/></title>
      </head>
      <body>
        <table>
          <tr>
            <xsl:for-each select="$schema/xsd:complexType[@name=$rowtypename]/xsd:sequence/xsd:element/@name">
              <th><xsl:value-of select="."/></th>
            </xsl:for-each>
          </tr>

          <xsl:for-each select="row">
            <tr>
              <xsl:for-each select="*">
                <td><xsl:value-of select="."/></td>
              </xsl:for-each>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
```

### 9.27. System Information Functions and Operators

https://www.postgresql.org/docs/current/functions-info.html

The functions described in this section are used to obtain various information about a PostgreSQL installation.

#### 9.27.1. Session Information Functions 

- `pg_backend_pid()` → `integer`
    Returns the process ID of the server process attached to the current session.

#### 9.27.4. System Catalog Information Functions 

- `pg_get_functiondef` ( *`func`* `oid` ) → `text`
    重构函数或过程的创建命令。（这是反编译重构，不是命令的原始文本。）结果是完整的 `CREATE OR REPLACE FUNCTION` 或 `CREATE OR REPLACE PROCEDURE` 语句。

### 9.28. System Administration Functions

## Chapter 27. Monitoring Database Activity

### 27.2. The Cumulative Statistics System

https://www.postgresql.org/docs/18/monitoring-stats.html

PostgreSQL 的*累积统计系统*支持收集和报告有关服务器活动的信息。目前，会统计对表和索引的磁盘块访问和单行访问。还会统计每个表中的总行数，以及有关每个表的 vacuum 和 analyze 操作的信息。如果启用，还会统计对用户定义函数的调用以及每个函数的總耗时。

PostgreSQL 还支持报告有关系统当前正在发生什么的动态信息，例如其他服务器进程当前正在执行的确切命令，以及系统中存在哪些其他连接。此功能独立于累积统计系统。

### 27.2.3. pg_stat_activity

`pg_stat_activity` 视图将为每个服务器进程提供一行，显示与该进程当前活动相关的信息。

**表 27.3. `pg_stat_activity` 视图**

- `datid` `oid`
  此后端连接到的数据库的 OID

- `datname` `name`
  此后端连接到的数据库的名称

- `pid` `integer`
  此后端的进程 ID

- `leader_pid` `integer`
  如果此进程是并行查询工作进程，则为并行组领导者的进程 ID；如果此进程是并行应用工作进程，则为领导者应用工作进程的进程 ID。`NULL` 表示此进程是并行组领导者或领导者应用工作进程，或者不参与任何并行操作。

- `usesysid` `oid`
  登录到此后端的用户的 OID

- `usename` `name`
  登录到此后端的用户的名称

- `application_name` `text`
  连接到此后端的应用程序的名称

- `client_addr` `inet`
  连接到此后端的客户端的 IP 地址。如果此字段为 null，则表示客户端通过服务器机器上的 Unix 套接字连接，或者这是一个内部进程（如 autovacuum）。

- `client_hostname` `text`
  已连接客户端的主机名，由 `client_addr` 的反向 DNS 查找报告。此字段仅在 IP 连接时非 null，并且仅在启用 [log_hostname] 时。

- `client_port` `integer`
  客户端用于与此后端通信的 TCP 端口号，如果使用 Unix 套接字则为 `-1`。如果此字段为 null，则表示这是一个内部服务器进程。

- `backend_start` `timestamp with time zone`
  此进程启动的时间。对于客户端后端，这是客户端连接到服务器的时间。

- `xact_start` `timestamp with time zone`
  此进程当前事务启动的时间，如果没有活动事务则为 null。如果当前查询是其事务的第一个查询，则此列等于 `query_start` 列。

- `query_start` `timestamp with time zone`
  当前活动查询启动的时间，或者如果 `state` 不是 `active`，则为上一个查询启动的时间

- `state_change` `timestamp with time zone`
  `state` 上次更改的时间

- `wait_event_type` `text`
  后端正在等待的事件类型（如果有）；否则为 NULL。参见 [表 27.4](monitoring-stats.html#WAIT-EVENT-TABLE)。

- `wait_event` `text`
  如果后端当前正在等待，则为等待事件名称，否则为 NULL。参见 [表 27.5](monitoring-stats.html#WAIT-EVENT-ACTIVITY-TABLE) 到 [表 27.13](monitoring-stats.html#WAIT-EVENT-TIMEOUT-TABLE)。

- `state` `text`
  此后端的当前总体状态。可能的值为：
  - `starting`：后端处于初始启动阶段。客户端身份验证在此阶段执行。
  - `active`：后端正在执行查询。
  - `idle`：后端正在等待新的客户端命令。
  - `idle in transaction`：后端处于事务中，但当前未执行查询。
  - `idle in transaction (aborted)`：此状态类似于 `idle in transaction`，只是事务中的某个语句导致了错误。
  - `fastpath function call`：后端正在执行快速路径函数。
  - `disabled`：如果此后端中禁用了 [track_activities](runtime-config-statistics.html#GUC-TRACK-ACTIVITIES)，则报告此状态。

- `backend_xid` `xid`
  此后端的顶层事务标识符（如果有）；参见[第 67.1 节](transaction-id.html)。

- `backend_xmin` `xid`
  当前后端的 `xmin` horizon。

- `query_id` `bigint`
  此后端最近查询的标识符。如果 `state` 为 `active`，此字段显示当前正在执行的查询的标识符。在所有其他状态下，它显示最后执行的查询的标识符。默认情况下不计算查询标识符，因此除非启用了 [compute_query_id](runtime-config-statistics.html#GUC-COMPUTE-QUERY-ID) 参数，或者配置了计算查询标识符的第三方模块，否则此字段将为 null。

- `query` `text`
  此后端最近查询的文本。如果 `state` 为 `active`，此字段显示当前正在执行的查询。在所有其他状态下，它显示最后执行的查询。默认情况下，查询文本截断为 1024 字节；此值可以通过参数 [track_activity_query_size] 更改。

- `backend_type` `text`
  当前后端的类型。可能的类型有 `autovacuum launcher`、`autovacuum worker`、`logical replication launcher`、`logical replication worker`、`parallel worker`、`background writer`、`client backend`、`checkpointer`、`archiver`、`standalone backend`、`startup`、`walreceiver`、`walsender`、`walwriter` 和 `walsummarizer`。此外，由扩展注册的后台工作进程可能有其他类型。

示例
- 查看当前语句
    ```sql
    SELECT query
    FROM pg_stat_activity
    WHERE pid = pg_backend_pid()
    ```

## Chapter 36. Extending SQL

### 36.7. Function Volatility Categories

https://www.postgresql.org/docs/current/xfunc-volatility.html

每个函数都有一个*易变性*（volatility）分类，可能为 `VOLATILE`、`STABLE` 或 `IMMUTABLE`。如果 [`CREATE FUNCTION`] 命令未指定类别，则默认为 `VOLATILE`。易变性类别是向优化器作出的关于函数行为的承诺：

- `VOLATILE` 函数可以做任何事，包括修改数据库。对于相同的参数，连续调用可能返回不同结果。优化器不会对此类函数的行为做任何假设。使用易变函数的查询会在需要其值的每一行重新计算该函数。

- `STABLE` 函数不能修改数据库，并且保证在单条语句内，对于所有行，给定相同参数时返回相同结果。此类别允许优化器将函数的多次调用优化为一次调用。特别是，在索引扫描条件中使用包含此类函数的表达式是安全的。（由于索引扫描只会计算一次比较值，而不是在每一行计算一次，因此在索引扫描条件中使用 `VOLATILE` 函数是无效的。）

- `IMMUTABLE` 函数不能修改数据库，并且保证对于给定相同参数永远返回相同结果。此类别允许优化器在查询以常量参数调用该函数时预先计算该函数。例如，类似 `SELECT ... WHERE x = 2 + 2` 的查询可以立即简化为 `SELECT ... WHERE x = 4`，因为整数加法运算符底层的函数被标记为 `IMMUTABLE`。

## Chapter 52. System Catalogs

### 52.11. pg_class

## 52.11. `pg_class`

目录 `pg_class` 描述表和具有列或以其他方式类似表的其他对象。这包括索引（另见 [`pg_index`]）、序列（另见 [`pg_sequence`]）、视图、物化视图、复合类型和 TOAST 表；参见 `relkind`。下文当我们指所有这些类型的对象时，我们称之为“关系”。并非 `pg_class` 的所有列对所有关系类型都有意义。

**表 52.11. `pg_class` 列**

- `oid` `oid`
  行标识符

- `relname` `name`
  表、索引、视图等的名称

- `relnamespace` `oid`（引用 [`pg_namespace`](catalog-pg-namespace.html).`oid`）
  包含此关系的命名空间的 OID

- `reltype` `oid`（引用 [`pg_type`](catalog-pg-type.html).`oid`）
  对应于此表行类型的数据类型的 OID（如果有）；对于索引、序列和 TOAST 表为零，这些没有 `pg_type` 条目

- `reloftype` `oid`（引用 [`pg_type`](catalog-pg-type.html).`oid`）
  对于类型化表，为底层复合类型的 OID；对于所有其他关系为零

- `relowner` `oid`（引用 [`pg_authid`](catalog-pg-authid.html).`oid`）
  关系的所有者

- `relam` `oid`（引用 [`pg_am`](catalog-pg-am.html).`oid`）
  用于访问此表或索引的访问方法。如果关系是序列或没有磁盘文件，则没有意义，但分区表除外；对于分区表，如果设置了此值，则在确定创建命令中未指定访问方法时创建分区所使用的访问方法时，它会优先于 `default_table_access_method`。

- `relfilenode` `oid`
  此关系的磁盘文件名；零表示这是一个“映射”关系，其磁盘文件名由底层状态确定

- `reltablespace` `oid`（引用 [`pg_tablespace`](catalog-pg-tablespace.html).`oid`）
  存储此关系的表空间。如果为零，则隐含数据库的默认表空间。如果关系没有磁盘文件，则没有意义，但分区表除外；对于分区表，这是创建命令中未指定分区时创建分区的表空间。

- `relpages` `int4`
  此表的磁盘表示大小，以页（大小为 `BLCKSZ`）为单位。这只是计划程序使用的估计值。它由 [`VACUUM`](sql-vacuum.html)、[`ANALYZE`](sql-analyze.html) 以及一些 DDL 命令（如 [`CREATE INDEX`](sql-createindex.html)）更新。

- `reltuples` `float4`
  表中的活行数。这只是计划程序使用的估计值。它由 [`VACUUM`](sql-vacuum.html)、[`ANALYZE`](sql-analyze.html) 以及一些 DDL 命令（如 [`CREATE INDEX`](sql-createindex.html)）更新。如果表从未被 vacuum 或 analyze 过，`reltuples` 包含 `-1`，表示行数未知。

- `relallvisible` `int4`
  表的可见性映射中标记为 all-visible 的页数。这只是计划程序使用的估计值。它由 [`VACUUM`](sql-vacuum.html)、[`ANALYZE`](sql-analyze.html) 以及一些 DDL 命令（如 [`CREATE INDEX`](sql-createindex.html)）更新。

- `relallfrozen` `int4`
  表的可见性映射中标记为 all-frozen 的页数。这只是用于触发 autovacuum 的估计值。它还可以与 `relallvisible` 一起用于调度手动 vacuum 和调整 [vacuum 的冻结行为](runtime-config-vacuum.html#RUNTIME-CONFIG-VACUUM-FREEZING)。它由 [`VACUUM`](sql-vacuum.html)、[`ANALYZE`](sql-analyze.html) 以及一些 DDL 命令（如 [`CREATE INDEX`](sql-createindex.html)）更新。

- `reltoastrelid` `oid`（引用 [`pg_class`](catalog-pg-class.html).`oid`）
  与此表关联的 TOAST 表的 OID，如果没有则为零。TOAST 表将大属性“行外”存储在辅助表中。

- `relhasindex` `bool`
  如果这是一个表并且它有（或最近有）任何索引，则为 true

- `relisshared` `bool`
  如果此表在集群中的所有数据库之间共享，则为 true。只有某些系统目录（如 [`pg_database`](catalog-pg-database.html)）是共享的。

- `relpersistence` `char`
  `p` = 永久表/序列，`u` = 未记录表/序列，`t` = 临时表/序列

- `relkind` `char`
  `r` = 普通表，`i` = 索引，`S` = 序列，`t` = TOAST 表，`v` = 视图，`m` = 物化视图，`c` = 复合类型，`f` = 外部表，`p` = 分区表，`I` = 分区索引

- `relnatts` `int2`
  关系中的用户列数（系统列不计）。[`pg_attribute`](catalog-pg-attribute.html) 中必须有这么多对应条目。另见 `pg_attribute`.`attnum`。

- `relchecks` `int2`
  表上的 `CHECK` 约束数；参见 [`pg_constraint`](catalog-pg-constraint.html) 目录

- `relhasrules` `bool`
  如果表有（或曾经有）规则，则为 true；参见 [`pg_rewrite`](catalog-pg-rewrite.html) 目录

- `relhastriggers` `bool`
  如果表有（或曾经有）触发器，则为 true；参见 [`pg_trigger`](catalog-pg-trigger.html) 目录

- `relhassubclass` `bool`
  如果表或索引有（或曾经有）任何继承子级或分区，则为 true

- `relrowsecurity` `bool`
  如果表启用了行级安全，则为 true；参见 [`pg_policy`](catalog-pg-policy.html) 目录

- `relforcerowsecurity` `bool`
  如果行级安全（启用时）也将应用于表所有者，则为 true；参见 [`pg_policy`](catalog-pg-policy.html) 目录

- `relispopulated` `bool`
  如果关系已填充，则为 true（对于除某些物化视图之外的所有关系，这都为 true）

- `relreplident` `char`
  用于形成行的“副本标识”的列：`d` = 默认（主键，如果有），`n` = 无，`f` = 所有列，`i` = 设置了 `indisreplident` 的索引（如果使用的索引已被删除，则与无相同）

- `relispartition` `bool`
  如果表或索引是分区，则为 true

- `relrewrite` `oid`（引用 [`pg_class`](catalog-pg-class.html).`oid`）
  对于在需要重写表的 DDL 操作期间正在写入的新关系，这包含原始关系的 OID；否则为零。该状态仅在内部可见；对于用户可见的关系，此字段绝不应包含零以外的任何值。

- `relfrozenxid` `xid`
  此事务 ID 之前的所有事务 ID 已在此表中被替换为永久（“冻结”）事务 ID。这用于跟踪是否需要 vacuum 表以防止事务 ID 回绕或允许收缩 `pg_xact`。如果关系不是表，则为零（`InvalidTransactionId`）。

- `relminmxid` `xid`
  此多事务 ID 之前的所有多事务 ID 已在此表中被事务 ID 替换。这用于跟踪是否需要 vacuum 表以防止多事务 ID 回绕或允许收缩 `pg_multixact`。如果关系不是表，则为零（`InvalidMultiXactId`）。

- `relacl` `aclitem[]`
  访问权限；详情参见[第 5.8 节](ddl-priv.html)

- `reloptions` `text[]`
  访问方法特定的选项，以“keyword=value”字符串表示

- `relpartbound` `pg_node_tree`
  如果表是分区（参见 `relispartition`），则为分区边界的内部表示

`pg_class` 中的几个布尔标志是延迟维护的：如果那是正确状态，则保证为 true，但当条件不再为 true 时，可能不会立即重置为 false。例如，`relhasindex` 由 [`CREATE INDEX`] 设置，但从不被 [`DROP INDEX`]清除。相反，如果 [`VACUUM`] 发现表没有索引，则会清除 `relhasindex`。这种安排避免了竞争条件并提高了并发性。

### 52.39. pg_proc

https://www.postgresql.org/docs/current/catalog-pg-proc.html

`pg_proc` 目录存储有关函数、过程、聚合函数和窗口函数（统称为例程）的信息。更多信息请参见 [`CREATE FUNCTION`]、[`CREATE PROCEDURE`] 和 [第 36.3 节 xfunc]。

如果 `prokind` 表明该条目是聚合函数，则应在 [`pg_aggregate`] 中存在匹配的行。

列 - 类型 - 描述
- `proname` `name`
    函数的名称
- `prosrc` `text` （CTF 中读取函数代码）
    这告诉函数处理程序如何调用该函数。它可能是解释型语言的实际源代码、链接符号、文件名，或几乎任何其他内容，具体取决于实现语言/调用约定。

对于编译函数，无论是内置的还是动态加载的，`prosrc` 都包含函数的 C 语言名称（链接符号）。对于 SQL 语言函数，如果以字符串字面量指定，`prosrc` 包含函数的源文本；但如果函数体以 SQL 标准风格指定，则 `prosrc` 未使用（通常为空字符串），而 `prosqlbody` 包含预解析的定义。对于所有其他当前已知的语言类型，`prosrc` 包含函数的源文本。`probin` 为空，动态加载的 C 函数除外；对于后者，它给出包含该函数的共享库文件名。

## Chapter 53. System Views

### 53.32. pg_tables

`pg_tables` 视图提供对数据库中每个表的有用信息的访问。

**表 53.32. `pg_tables` 列**

- `schemaname` `name`（引用 [`pg_namespace`](catalog-pg-namespace.html).`nspname`）
  包含表的模式名称

- `tablename` `name`（引用 [`pg_class`](catalog-pg-class.html).`relname`）
  表名称

- `tableowner` `name`（引用 [`pg_authid`](catalog-pg-authid.html).`rolname`）
  表所有者的名称

- `tablespace` `name`（引用 [`pg_tablespace`](catalog-pg-tablespace.html).`spcname`）
  包含表的表空间名称（如果为数据库默认则为 null）

- `hasindexes` `bool`（引用 [`pg_class`](catalog-pg-class.html).`relhasindex`）
  如果表有（或最近有）任何索引，则为 true

- `hasrules` `bool`（引用 [`pg_class`](catalog-pg-class.html).`relhasrules`）
  如果表有（或曾经有）规则，则为 true

- `hastriggers` `bool`（引用 [`pg_class`](catalog-pg-class.html).`relhastriggers`）
  如果表有（或曾经有）触发器，则为 true

- `rowsecurity` `bool`（引用 [`pg_class`](catalog-pg-class.html).`relrowsecurity`）
  如果表上启用了行级安全，则为 true