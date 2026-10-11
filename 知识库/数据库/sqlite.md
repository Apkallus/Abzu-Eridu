https://sqlite.org/schematab.html  

## 待拆分

创建一个临时表，并取出列
```sql
WITH tmp_table AS (SELECT tmp_value AS tmp_col)
SELECT tmp_col FROM tmp_table;
```

SQLite 允许在 WITH 里放 `UPDATE ... RETURNING ...`，把“UPDATE 修改的行”当成一个临时结果集再 SELECT 出来。然而可写 CTE（包含 UPDATE、INSERT 或 DELETE 的 CTE）必须位于 SQL 语句的顶层：
(此处对用户名 bob 写回原password)
```sql
WITH t AS (
  UPDATE users
  SET password=password
  WHERE username='bob'
  RETURNING username
)
SELECT username FROM t;
```
- RETURNING 的作用：让 UPDATE 产生“可被 SELECT 读取”的输出。


枚举所有SQL函数 `pragma_function_list`：
`SELECT name, type, flags FROM pragma_function_list`
- `type`：函数类型（`s`表示标量函数，`w`表示聚合函数）。
- `flags`：标志位，其中 `directonly` 标志表示该函数只能从顶层SQL调用
- 常见的危险函数名称及用途：
  - `load_extension`：动态加载SQLite扩展（`.so`、`.dll`文件），这是执行系统命令的关键。
  - `readfile` / `writefile`：在某些扩展（如`sqlean-fileio`）或自定义编译版本中，用于直接读写服务器文件。


查看编译选项 `pragma_compile_options`
该pragma可以列出SQLite编译时启用的所有选项，判断环境是否支持动态加载。
`SELECT compile_options FROM pragma_compile_options`
- `ENABLE_LOAD_EXTENSION`：如果存在此选项，说明允许通过`load_extension()`函数加载外部动态库。
- `OMIT_LOAD_EXTENSION`：如果存在此选项，则说明编译时禁用了动态加载，通常意味着`load_extension`函数不可用。


概念：SQLite 扩展 / load_extension
- SQLite 扩展本质是一个共享库 `.so`。
- 执行 `SELECT load_extension('/path/ext.so')`，SQLite 会 `dlopen()` 这个库，并调用一个约定入口函数（通常叫 `sqlite3_extension_init`）。
- 在这个 `init` 函数里，扩展可以调用 SQLite API（如 `sqlite3_create_function`）向当前连接注册新 SQL 函数。
- 后续就能在 SQL 里调用注册的函数：`SELECT myfunc(...)`。

## ⚔️ The Schema Table —— 模式表

https://sqlite.org/schematab.html

### 1. 简介

每个 SQLite 数据库都包含一个单独的“模式表”，用于存储该数据库的模式。数据库模式是对数据库中所有其他表、索引、触发器和视图的描述。模式表的结构如下：

```sql
CREATE TABLE sqlite_schema(
  type text,
  name text,
  tbl_name text,
  rootpage integer,
  sql text
);
```

`sqlite_schema` 表为模式中的每个表、索引、视图和触发器（统称为“对象”）包含一行记录，但 `sqlite_schema` 表本身除外。有关 SQLite 如何在内部使用 `sqlite_schema` 表的更多信息，请参阅 [文件格式] 文档中的 [模式存储] 子章节。

### 2. 别名

模式表始终可以使用名称 `sqlite_schema` 引用，特别是当通过模式名称限定时，如 `main.sqlite_schema` 或 `temp.sqlite_schema`。但为了历史兼容性，也识别以下别名：

1.  `sqlite_master` ⚔️
2.  `sqlite_temp_schema`
3.  `sqlite_temp_master`

别名 (2) 和 (3) 仅适用于与每个数据库连接关联的 TEMP 数据库，而别名 (1) 在任何地方都有效。

出于历史原因，来自 [`sqlite3_set_authorizer()`] 接口的回调始终使用名称 (1) 或 (3) 引用模式表。

### 3. 模式表的解读

模式表各字段的含义如下：

-   type

    `sqlite_schema.type` 列将是以下文本字符串之一：`'table'`、`'index'`、`'view'` 或 `'trigger'`，具体取决于所定义对象的类型。`'table'` 字符串用于普通表和 [虚拟表]。

-   name ⚔️

    `sqlite_schema.name` 列将保存对象的名称。表上的 [UNIQUE] 和 [PRIMARY KEY] 约束会导致 SQLite 创建名为 `sqlite_autoindex_TABLE_N` 形式的 [内部索引]，其中 TABLE 被替换为包含约束的表的名称，N 是一个从 1 开始并随表定义中看到的每个约束递增的整数。

    在 [WITHOUT ROWID] 表中，PRIMARY KEY 没有 `sqlite_schema` 条目，但 `sqlite_autoindex_TABLE_N` 名称会被预留用于 PRIMARY KEY，就像 `sqlite_schema` 条目存在一样。这将影响后续 UNIQUE 约束的编号。

    `sqlite_autoindex_TABLE_N` 名称永远不会分配给 [INTEGER PRIMARY KEY]，无论是在 rowid 表还是 WITHOUT ROWID 表中。

-   tbl_name

    `sqlite_schema.tbl_name` 列保存与该对象关联的表或视图的名称。对于表或视图，`tbl_name` 列是 `name` 列的副本。对于索引，`tbl_name` 是被索引的表的名称。对于触发器，`tbl_name` 列存储导致触发器触发的表或视图的名称。

-   rootpage

    `sqlite_schema.rootpage` 列存储表和索引的根 b-tree 页的页号。对于定义视图、触发器和虚拟表的行，`rootpage` 列为 0 或 NULL。

-   sql ⚔️

    `sqlite_schema.sql` 列存储描述对象的 SQL 文本。此 SQL 文本是一条 [CREATE TABLE]、[CREATE VIRTUAL TABLE]、[CREATE INDEX]、[CREATE VIEW] 或 [CREATE TRIGGER] 语句，如果针对作为 [数据库连接] 主数据库的数据库文件执行该语句，将重新创建该对象。该文本通常是用于创建对象的原始语句的副本，但经过规范化以符合以下规则：

    -   语句开头的 CREATE、TABLE、VIEW、TRIGGER 和 INDEX 关键字转换为大写字母。
    -   如果 TEMP 或 TEMPORARY 关键字出现在初始 CREATE 关键字之后，则将其移除。
    -   移除出现在正在创建的对象名称之前的任何数据库名称限定符。
    -   移除前导空格。
    -   将前两个关键字之后的所有空格转换为单个空格。

    `sqlite_schema.sql` 列中的文本是创建对象的原始 CREATE 语句文本的副本，除了如上所述进行规范化以及由后续 [ALTER TABLE] 语句修改外。

    对于由 [UNIQUE] 或 [PRIMARY KEY] 约束自动创建的 [内部索引]，`sqlite_schema.sql` 为 NULL。

### 4. 模式表的创建与修改

SQLite 在创建数据库时创建模式表，并在 SQLite 用户提交 DDL 语句执行时修改其内容。在正常情况下，用户无需修改它，如果修改它，他们将承担 [数据库损坏] 的风险。

本页最后更新时间：2023-06-16 10:11:06Z
