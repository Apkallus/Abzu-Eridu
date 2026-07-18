#### Cookie 投掷漏洞

如果攻击者设法控制任何子域，此漏洞的影响可能很广泛，包括攻击者固定会话令牌，从而导致帐户接管。以下是攻击的工作原理（攻击者子域设置目标父域 cookie，设置较长 path 确保优先使用）：

**步骤 1**：控制 `vulnerable.example.com` 的攻击者将名为“sessionID”的 Cookie 设置为已知值。

**示例**

```
Set-Cookie: sessionID=valueknowntoattacker; domain=example.com
```

**步骤 2**：当受害者访问攻击者控制的子域（`vulnerable.example.com`）时，浏览器存储该值。

**步骤 3**：受害者访问 `example.com` 并使用固定的会话 ID 登录应用程序。

**步骤 4**：当受害者登录应用程序时，应用程序不会生成新的 SessionID。

**步骤 5**：攻击者使用相同的会话 ID 接管受害者的帐户。

即使已经设置了具有特定名称的 Cookie，Cookie 投掷也是可能的。当浏览器收到两个同名的 Cookie 时，浏览器会将请求视为有效并同时发送两者。

**示例**

```
Set-Cookie: SessionID=setbytheserver; SessionID=attackerknow; domain=.example.com
```

大多数应用程序在重复的情况下将处理第一个参数。在这种情况下，我们可以通过添加更长的路径来强制我们的 Cookie。这是因为根据 RFC 6265 的文档，路径较长的 Cookie 具有优先权（[https://datatracker.ietf.org/doc/html/rfc6265#section-5.4](https://datatracker.ietf.org/doc/html/rfc6265#section-5.4)）。

**图 1.6 RFC 6265 关于 Cookie 顺序的摘录**

**较短路径的示例**

```
Set-Cookie: SessionID=setbytheserver; domain=.example.com; path=/
```

**攻击者设置较长路径的示例**

```
Set-Cookie: SessionID=attackerknow; domain=.example.com; path=/admin
```

当浏览器处理这些标头时，它将存储两个 Cookie。但是，当访问同时匹配两个 Cookie 的路径（如 `/admin`）时，由攻击者设置的具有较长路径的 Cookie 将优先。
