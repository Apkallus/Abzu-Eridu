```sql
SELECT column1, column2, ...
FROM table_name
WHERE condition
```

```sql
UPDATE table_name 
SET column1 = value1, column2 = value2,... 
WHERE condition
```

```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    column3 datatype,
   ....
)
```
```sql
CREATE TABLE table_name AS
SELECT the_data AS colume_name
```
`AS`:
- 创建表时 `CREATE TABLE table_name AS SELECT ...`  
    其中 `AS` 关键字是 `CREATE TABLE AS SELECT` 语法的一部分：“把这个 SELECT 的结果当成表来创建”。
- 其他上下文的 `AS` 关键字用于为列或表指定一个别名

```sql
ALTER TABLE table_name
ADD column_name datatype
```

```sql
GRANT 权限 ON 对象名（表名） TO 用户名
```

```sql
DROP TABLE table_name
```

在SQL中，`And`运算符的优先级高于`Or`运算符
不等于：
- `1 <> 2`
- `1 != 2`

`%` 通配符

`substr(some_column, start, length)` 会从 `some_column` 列的第 `start` 个字符开始（第一个字符的位置是 `1`）提取 `length` 个字符。

各sql对单双引号的支持不同：
- SQLite
    - 单双引号完全兼容
- PostgreSQL / SQL Server / Oracle
    - 单引号
    - 双引号仅可作为标识符（列名、表名），当字符串 ❌ 语法错误
- MySQL
    - 单双引号可完全兼容
    - 若开启`ANSI_QUOTES`模式则使用标准SQL，双引号仅可作为标识符，当字符串 ❌ 语法错误

NULL 值：
- `IS NULL` 判断是否为 NULL
- `IFNULL(expression, replacement_value)` 非标准
    如果为空，则替换
- `COALESCE(expr1, expr2, expr3, ...)`  标准
    从左到右依次检查每个参数，一旦遇到第一个非 NULL 的值，就立即返回该值并停止后续计算。如果所有参数都是 NULL，则返回 NULL。

聚合函数 `group_concat()`
把所有行合并成一个用逗号分隔的字符串

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ...
    ELSE default_result
END
```

## 引用

- [w3schools SQL](https://www.w3schools.com/SQL)