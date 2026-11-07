https://sqlite.org/schematab.html

# Schema 表

**目录**

- “1. 简介”
- “2. 替代名称”
- “3. Schema 表的解释”
- “4. Schema 表的创建与修改”

## 1. 简介

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

`sqlite_schema` 表为 schema 中的每个表、索引、视图和触发器（统称为“对象”）包含一行，但 `sqlite_schema` 表本身没有对应条目。有关 SQLite 如何在内部使用 `sqlite_schema` 表的更多信息，请参阅“文件格式”文档中的“模式存储”小节。

## 2. 替代名称

schema 表始终可以使用名称 `sqlite_schema` 引用，特别是在用 schema 名称限定它时，例如 `main.sqlite_schema` 或 `temp.sqlite_schema`。但为了历史兼容性，也识别一些替代名称，包括：

1. `sqlite_master`
2. `sqlite_temp_schema`
3. `sqlite_temp_master`

替代名称 (2) 和 (3) 仅适用于与每个数据库连接关联的 `TEMP` 数据库，但替代名称 (1) 在任何地方都有效。由于历史原因，来自 `sqlite3_set_authorizer()` 接口的回调始终使用名称 (1) 或 (3) 来引用 schema 表。

## 3. Schema 表的解释

schema 表各字段的含义如下：

- `type`  
  根据所定义对象的类型，`sqlite_schema.type` 列将是以下文本字符串之一：`'table'`、`'index'`、`'view'` 或 `'trigger'`。字符串 `'table'` 用于普通表和“虚拟表”。

- `name`  
  `sqlite_schema.name` 列保存对象的名称。表上的 `UNIQUE` 和 `PRIMARY KEY` 约束会使 SQLite 创建“内部索引”，其名称形式为 `sqlite_autoindex_TABLE_N`，其中 `TABLE` 替换为包含该约束的表的名称，`N` 是一个从 1 开始的整数，并随着表定义中出现的每个约束递增一。在 `WITHOUT ROWID` 表中，`PRIMARY KEY` 没有对应的 `sqlite_schema` 条目，但会为 `PRIMARY KEY` 预留 `sqlite_autoindex_TABLE_N` 名称，就好像该 `sqlite_schema` 条目确实存在一样。这会影响后续 `UNIQUE` 约束的编号。对于 `INTEGER PRIMARY KEY`，无论是在 `rowid` 表还是 `WITHOUT ROWID` 表中，都不会分配 `sqlite_autoindex_TABLE_N` 名称。

- `tbl_name`  
  `sqlite_schema.tbl_name` 列保存对象所关联的表或视图的名称。对于表或视图，`tbl_name` 列是 `name` 列的副本。对于索引，`tbl_name` 是被索引的表的名称。对于触发器，`tbl_name` 列存储导致触发器触发的表或视图的名称。

- `rootpage`  
  `sqlite_schema.rootpage` 列存储表和索引的根 b-tree 页面的页码。对于定义视图、触发器和虚拟表的行，`rootpage` 列为 0 或 `NULL`。

- `sql`  
  该列存储描述对象的 SQL 文本。该 SQL 文本是一个 `CREATE TABLE`、`CREATE VIRTUAL TABLE`、`CREATE INDEX`、`CREATE VIEW` 或 `CREATE TRIGGER` 语句；如果在该数据库文件作为“数据库连接”的 `main` 数据库时对其求值，该语句将重新创建该对象。该文本通常是用于创建对象的原始语句的副本，但会应用规范化，使文本符合以下规则：

    - 语句开头的 `CREATE`、`TABLE`、`VIEW`、`TRIGGER` 和 `INDEX` 关键字会转换为全大写字母。
    - 如果 `TEMP` 或 `TEMPORARY` 关键字出现在初始 `CREATE` 关键字之后，则将其移除。
    - 删除创建对象名称之前出现的任何数据库名称限定符。
    - 删除前导空格。
    - 前两个关键字之后的所有空格转换为单个空格。

  `sqlite_schema.sql` 列中的文本是创建该对象的原始 `CREATE` 语句文本的副本，但会按上述方式规范化，并会反映后续 `ALTER TABLE` 语句所做的修改。对于由 `UNIQUE` 或 `PRIMARY KEY` 约束自动创建的“内部索引”，`sqlite_schema.sql` 为 `NULL`。

## 4. Schema 表的创建与修改

SQLite 在创建数据库时创建 schema 表，并在 SQLite 用户提交 `DDL` 语句以供执行时修改其内容。正常情况下，用户无需修改它；如果用户确实修改了它，则需承担“数据库损坏”的风险。

*本页最后更新于 2023-06-16 10:11:06Z*