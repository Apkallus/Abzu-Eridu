### 第 4 步：寻找 NoSQL 注入

数据库并不总是使用 SQL。NoSQL（Not Only SQL）数据库是指不使用 SQL 语言的数据库。与将数据存储在表中的 SQL 数据库不同，NoSQL 数据库将数据存储在其他结构中，如键值对和图。NoSQL 查询语法因数据库而异，查询通常用应用程序的编程语言编写。现代 NoSQL 数据库，如 MongoDB、Apache CouchDB 和 Apache Cassandra，也容易受到注入攻击。随着 NoSQL 越来越流行，这些漏洞也越来越常见。

以 MongoDB 为例。在 MongoDB 语法中，`Users.find()` 返回满足特定条件的用户。例如，以下查询返回用户名为 `vickie`、密码为 `password123` 的用户：

```javascript
Users.find({username: 'vickie', password: 'password123'});
```

如果应用程序使用此功能登录用户，并直接用用户输入填充数据库查询，如下所示：

```javascript
Users.find({username: $username, password: $password});
```

攻击者可以提交密码 `{$ne: ""}` 以任何人的身份登录。例如，假设攻击者提交用户名为 `admin`，密码为 `{$ne: ""}`。数据库查询将变为：

```javascript
Users.find({username: 'admin', password: {$ne: ""}});
```

在 MongoDB 中，`$ne` 选择值不等于指定值的对象。这里，查询将返回用户名为 `admin` 且密码不等于空字符串的用户，除非 admin 的密码为空，否则该条件为真！攻击者因此可以绕过身份验证并访问 admin 账户。

向 MongoDB 查询注入还可以允许攻击者在服务器上执行任意 JavaScript 代码。在 MongoDB 中，`$where`、`mapReduce`、`$accumulator` 和 `$function` 操作允许开发人员运行任意 JavaScript。例如，你可以在 `$where` 操作符中定义一个函数来查找名为 `vickie` 的用户：

```javascript
Users.find( { $where: function() {
  return (this.username == 'vickie') } } );
```

假设开发人员允许在此函数中传入未验证的用户输入，并用它来获取账户数据，如下所示：

```javascript
Users.find( { $where: function() {
  return (this.username == $user_input) } } );
```

在这种情况下，攻击者可以通过向 `$where` 操作注入任意 JavaScript 代码来执行它。例如，以下恶意代码将通过触发永不结束的 `while` 循环发起拒绝服务（DoS）攻击：

```javascript
Users.find( { $where: function() {
  return (this.username == 'vickie'; while(true){};) } } );
```

寻找 NoSQL 注入的过程类似于检测 SQL 注入。你可以在用户输入字段中插入特殊字符，如引号（`'`、`"`）、分号（`;`）、反斜杠（`\`）以及括号（`()`）、方括号（`[]`）和花括号（`{}`），并查找错误或其他异常。你也可以使用工具 NoSQLMap（https://github.com/codingo/NoSQLMap/）自动化寻找过程。

开发人员可以通过验证用户输入和避免危险的数据库功能来防止 NoSQL 注入攻击。在 MongoDB 中，你可以通过在命令行中使用 `--noscripting` 选项或将配置文件中的 `security.javascriptEnabled` 标志设置为 `false` 来禁用服务器端 JavaScript 的运行。更多信息请访问 https://docs.mongodb.com/manual/faq/fundamentals/index.html。

此外，在给应用程序分配权限时，应遵循最小权限原则。这意味着应用程序应仅以其运行所需的最小权限运行。例如，当应用程序仅需要读取文件时，不应授予任何写入或执行权限。这将降低攻击期间系统完全受损的风险。


