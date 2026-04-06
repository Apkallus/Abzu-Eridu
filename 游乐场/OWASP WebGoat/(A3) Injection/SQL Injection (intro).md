---
id: 
title: SQL Injection (intro)
---
<!-- muse start -->
Web Goat 的 SQL 注入简介
<!-- muse end -->

## 什么是 SQL？

SQL 是一种标准化编程语言（1986年成为ANSI标准，1987年成为ISO标准），用于管理关系型数据库并对其中的数据进行各种操作。

数据库是数据的集合。数据被组织成行、列和表的形式，并通过索引机制提高信息检索效率。

以下是一个包含员工数据的 SQL 表示例，表名为 `employees`：

**员工表**
 	 	 	 	 	 	
| userid | first_name | last_name | department  | salary  | auth_tan |
| ------ | ---------- | --------- | ----------- | ------- | -------- |
| 32147  | Paulina    | Travers   | Accounting  | $46,000 | P45JSI   |
| 89762  | Tobi       | Barnett   | Development | $77,000 | TA9LL1   |
| 96134  | Bob        | Franco    | Marketing   | $83,700 | LO9S2V   |
| 34477  | Abraham    | Holman    | Development | $50,000 | UU2ALK   |
| 37648  | John       | Smith     | Marketing   | $64,350 | 3SL99A   |

企业数据库存储的员工信息包含：唯一员工编号（'员工ID'）、姓氏、名字、部门、薪资和交易认证码（'auth_tan'）。每个信息字段存储在独立列中，每行代表一名公司员工。

SQL 查询可用于修改数据库表及其索引结构，并实现数据的增删改操作。

SQL 命令主要分为三类：
- 数据操作语言（DML）
- 数据定义语言（DDL）
- 数据控制语言（DCL）

攻击者可能利用这些命令类型破坏系统的保密性、完整性和/或可用性。继续学习课程以了解 SQL 命令类型及其与保护目标的关联。

若需更多 SQL 学习资源，可访问 [http://www.sqlcourse.com/](http://www.sqlcourse.com/) 获取免费交互式在线培训。

### 实践任务

请根据示例表，尝试检索员工 Bob Franco 所在的部门。注意：本练习中您已被授予完全管理员权限，无需认证即可访问所有数据。

根据信息构建 sql 语句：
```sql
SELECT department FROM Employees WHERE first_name='Bob'
```

## 数据操作语言（DML）

顾名思义，数据操作语言用于对数据进行操作。包括 SELECT、INSERT、UPDATE 和 DELETE 在内的多种常见 SQL 语句均属于 DML 语句范畴。DML 语句可用于查询记录（SELECT）、添加记录（INSERT）、删除记录（DELETE）以及修改现有记录（UPDATE）。

若攻击者成功将 DML 语句"注入"SQL 数据库，即可通过以下方式破坏系统安全：
- 使用 SELECT 语句破坏**保密性**
- 使用 UPDATE 语句破坏**完整性**  
- 使用 DELETE 或 UPDATE 语句破坏**可用性**

### DML 核心命令
- **SELECT** - 从数据库检索数据
- **INSERT** - 向数据库插入数据
- **UPDATE** - 更新数据库中的现有数据
- **DELETE** - 从数据库删除记录

### 语法示例

```sql
-- 数据检索示例：
SELECT phone
FROM employees
WHERE userid = 96134;
-- 该语句用于检索员工ID为96134的电话号码
```

### 实践任务

尝试将 Tobi Barnett 的部门修改为 "Sales"。注意：本练习中您已被授予完全管理员权限，无需认证即可访问所有数据。

构建 SQL 语句：
```sql
UPDATE Employees
SET department = 'Sales'
WHERE first_name = 'Tobi'
```

## 数据定义语言（DDL）

数据定义语言包含用于定义数据结构的命令。DDL 命令通常用于定义数据库的模式。模式指的是数据库的整体结构或组织方式，在 SQL 数据库中包括表、索引、视图、关系、触发器等对象。

若攻击者成功将 DDL 类型 SQL 命令"注入"数据库，可通过以下方式破坏系统安全：
- 使用 ALTER 和 DROP 语句破坏完整性
- 使用 DROP 语句破坏可用性

### DDL 核心命令

- CREATE - 创建数据库对象（如表和视图）
- ALTER - 修改现有数据库的结构
- DROP - 从数据库中删除对象

### 语法示例

```sql
CREATE TABLE employees(
    userid varchar(6) not null primary key,
    first_name varchar(20),
    last_name varchar(20),
    department varchar(20),
    salary varchar(10),
    auth_tan varchar(6)
);
-- 该语句创建了第2页所示的员工示例表
```

### 实践任务

请尝试通过添加 “phone” 列（varchar(20)）来修改 “employees” 表的模式。

构建 SQL 语句
```sql
ALTER TABLE employees
ADD phone varchar(20)
```


## 数据控制语言（DCL）

数据控制语言用于实现数据库中的访问控制逻辑。DCL 可用于收回和授予用户对表、视图、函数等数据库对象的访问权限。

若攻击者成功将 DCL 类型 SQL 命令"注入"数据库，可通过以下方式破坏系统安全：
- 使用 GRANT 命令破坏保密性
- 使用 REVOKE 命令破坏可用性

例如，攻击者可为自己授予数据库管理员权限，或撤销真实管理员的权限。

### DCL 核心命令

- GRANT - 授予用户对数据库对象的访问权限
- REVOKE - 收回通过 GRANT 授予的用户权限

### 实践任务

请尝试将表 `grant_rights` 的访问权限授予用户 `unauthorized_user`。

构建 SQL 语句
```sql
GRANT SELECT ON grant_rights TO unauthorized_user
```

## 什么是 SQL 注入？

SQL 注入（亦称 SQLi）是最常见的网络攻击技术之一。SQL 注入攻击通过将恶意代码从客户端插入到应用程序的 SQL 查询输入中实现。若未正确处理，SQL 注入可能严重危害数据完整性和安全性。

当来自客户端的未过滤数据（如搜索框输入）进入应用程序的 SQL 解释器时，就可能发生 SQL 注入。如果应用程序未能正确对用户输入进行消毒处理（如使用预处理语句）或过滤特殊字符，攻击者即可操纵底层 SQL 语句实现恶意目的。

例如，若未对 SQL 元字符（如 `--` 注释符或 `;` 查询结束符）进行过滤，就会导致 SQL 注入漏洞。

### SQL 注入示例

假设某网络应用允许用户通过在表单字段输入用户名来查询用户信息。用户输入被发送至服务器并嵌入 SQL 查询语句，最后由 SQL 解释器执行。

数据库查询语句如下：
```sql
"SELECT * FROM users WHERE name = '" + userName + "'";
```

变量 `userName` 承载客户端输入并将其"注入"查询语句。

若输入为 `Smith`，则查询变为：
```sql
"SELECT * FROM users WHERE name = 'Smith'";
```

此时将返回所有名为 Smith 的用户数据。

若攻击者输入包含 SQL 解释器特殊字符（如 `;`、`--` 或 `'`）的数据，且数据未经正确消毒或验证，攻击者即可修改 SQL 查询的预期行为，对数据库执行其他恶意操作。

### 攻击载荷示例

SQL 注入的危害远不止读取单个用户数据。以下是攻击者可能输入的恶意载荷示例：

- `Smith' OR '1' = '1`
  ```sql
  SELECT * FROM users WHERE name = 'Smith' OR TRUE;
  ```
  将返回用户表所有记录

- `Smith' OR 1 = 1; --`
  ```sql
  SELECT * FROM users WHERE name = 'Smith' OR TRUE;--';
  ```
  与第一个示例效果相同，返回全表数据

- `Smith'; DROP TABLE users; TRUNCATE audit_log; --`
  通过链式 SQL 命令同时删除用户表并清空审计日志表

### 数据库特性差异（以 SQL Server 为例）

- 命令执行能力：`master.dbo.xp_cmdshell 'cmd.exe dir c:'`
- 注册表操作命令：`xp_regread`、`xp_regdeletekey` 等


## 实践练习 字符串型 SQL 注入

代码中的查询语句通过字符串拼接方式构建动态查询（如前文示例所示），这种构造方式使其易受字符串型 SQL 注入攻击：
```js
"SELECT * FROM user_data WHERE first_name = 'John' AND last_name = '" + lastName + "'";
```
请尝试使用下方的表单检索用户表中的所有记录。注意：您无需知晓具体用户名即可获取完整列表。

完成提供的 SQL 语句，注入 `' or '1' = '1'`，sql的`and`运算符优先级高于`or`运算符
```sql
SELECT * FROM user_data WHERE first_name = 'John' and last_name = '' or '1' = '1'
```

## 实践练习 数字 SQL 注入

如前一个示例所示，代码中的查询通过拼接数字来构建动态查询，这使其容易受到数字SQL注入的攻击：

```js
"SELECT * FROM user_data WHERE login_count = " + Login_Count + " AND userid = "  + User_ID;
```

请使用下面的两个输入字段，尝试从users表中检索所有数据。

警告：只有其中一个字段容易受到SQL注入。您需要找出是哪一个，才能成功检索所有数据。

对两个字段进行测试，`Login_Count` 参数仅可为数字，`User_ID`字段可注入字符
构建最终 SQL，在 `User_ID`字段注入 `1 or 1=1`
```sql
SELECT * From user_data WHERE Login_Count = 1 and userid= 1 or 1=1
```


## 利用字符串型 SQL 注入破坏保密性

若系统存在 SQL 注入漏洞，其 CIA 三元组的安全属性可能轻易遭到破坏（若对 CIA 三元组概念不熟悉，可参考通用分类中的相关课程）。接下来三节课程将演示如何通过字符串型 SQL 注入或查询链技术分别破坏 CIA 三元组的各个维度。

本节课重点探讨保密性。攻击者利用 SQL 注入可轻易破坏保密性；例如，成功的 SQL 注入可使攻击者从数据库中读取信用卡号等敏感数据。

### 字符串型 SQL 注入原理

若应用程序仅通过简单拼接用户输入的字符串来构建 SQL 查询，则极易受到字符串型 SQL 注入攻击。具体而言，若用户输入的字符串未经任何消毒或预处理即被直接拼接到 SQL 查询中，攻击者仅需在输入字段中插入引号即可改变查询行为。例如，可通过引号提前结束字符串参数，并在其后注入自定义 SQL 代码。

### 实践任务

假设您是某大型企业的员工 John Smith。公司内部系统允许员工查看个人内部数据（如所属部门及薪资），但需使用唯一认证 TAN 码进行身份验证。您当前的 TAN 码为 `3SL99A`。

由于您迫切想了解自己是否为最高薪资员工，需要利用系统漏洞查看所有同事的薪资数据（而非仅限个人数据）。

请使用下方表单，尝试从员工表中检索所有员工数据。注意：您无需知晓具体姓名或 TAN 码即可获取所需信息。
已知执行查询的语句结构如下：
```js
"SELECT * FROM employees WHERE last_name = '" + name + "' AND auth_tan = '" + auth_tan + "'";
```

构建查询语句，在 `name`字段中注入`' or 1=1 --`

## 利用查询链技术破坏数据完整性

在上一课破坏了数据的保密性之后，本节课我们将通过 SQL 查询链技术来破坏数据的完整性。

若存在足够严重的漏洞，SQL 注入可被用于破坏数据库中任何数据的完整性。成功的 SQL 注入可能允许攻击者修改其本无权访问的信息。

### 什么是 SQL 查询链？

查询链即字面含义：通过追加一个或多个查询到实际查询末尾实现攻击。可使用元字符 `;` 实现此操作。分号 `;` 标记 SQL 语句的结束，使攻击者能在初始查询后立即开始新查询，无需换行。

### 实践任务

您刚发现 Tobi 和 Bob 的薪资似乎都比您高！这当然不能容忍。
请立即修改您自己的薪资，确保您成为最高收入者！

提示：您的姓名为 John Smith，当前 TAN 码为 3SL99A。

构建 `Employee Name` 字段的注入语句
```text
'; UPDATE employees 
SET SALARY=99999 
WHERE auth_tan='3SL99A'--
```

## 破坏可用性

在前几课成功破坏保密性和完整性的基础上，本节课我们将针对 CIA 三元组的第三个要素——可用性——展开攻击。

破坏可用性的方式多种多样。例如：若某个账户被删除或其密码被篡改，真实所有者将无法再访问该账户；攻击者也可尝试删除部分数据库内容，甚至直接删除整个数据库，使数据彻底不可用；此外，通过撤销管理员或其他用户的访问权限也是破坏可用性的常见手段——这将阻止相关用户访问数据库的特定部分乃至整个数据库。

### 实践任务

现在您已是公司最高薪资获得者。但请注意：系统中存在一个名为 `access_log` 的表，您所有的操作都被记录其中！
请立即在该表被他人查阅前，彻底清除所有日志记录。

在日志搜索功能中注入语句
`';DROP TABLE access_log--`