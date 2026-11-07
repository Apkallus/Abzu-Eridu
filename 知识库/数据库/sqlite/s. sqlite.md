https://sqlite.org/docs.html

[SQL 语言表达式（语法、运算优先级、操作符）](https://www.sqlite.org/lang_expr.html)

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

##  The Schema Table —— 模式表 ⚔️

https://sqlite.org/schematab.html

### 1. 简介

每个 SQLite 数据库都包含一个单一的“schema 表”，用于存储该数据库的 schema。数据库的 schema 是对该数据库中包含的所有其他表、索引、触发器和视图的描述。schema 表如下所示：

```sql
CREATE TABLE sqlite_schema(
  type text,
  name text,
  tbl_name text,
  rootpage integer,
  sql text
);
```

### 2. 替代名称

schema 表始终可以使用名称 `sqlite_schema` 引用，特别是在用 schema 名称限定它时，例如 `main.sqlite_schema` 或 `temp.sqlite_schema`。

### 3. Schema 表的解释

schema 表各字段的含义如下：

- `type`  
  根据所定义对象的类型，`sqlite_schema.type` 列将是以下文本字符串之一：`'table'`、`'index'`、`'view'` 或 `'trigger'`。字符串 `'table'` 用于普通表和“虚拟表”。

- `name`  
  `sqlite_schema.name` 列保存对象的名称。

- `sql`  
  该列存储描述对象的 SQL 文本。该 SQL 文本是一个 `CREATE TABLE`、`CREATE VIRTUAL TABLE`、`CREATE INDEX`、`CREATE VIEW` 或 `CREATE TRIGGER` 语句
  
  该文本通常是用于创建对象的原始语句的副本，但会应用规范化，并会反映后续 `ALTER TABLE` 语句所做的修改。对于由 `UNIQUE` 或 `PRIMARY KEY` 约束自动创建的“内部索引”，`sqlite_schema.sql` 为 `NULL`。
