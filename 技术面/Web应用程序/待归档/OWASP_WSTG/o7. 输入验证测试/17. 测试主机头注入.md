# 测试主机头注入

|ID          |
|------------|
|WSTG-INPV-17|

## 概述

Web 服务器通常在同一 IP 地址上托管多个 Web 应用程序，并通过虚拟主机来区分每个应用程序。在传入的 HTTP 请求中，Web 服务器通常根据 Host 头中提供的值将请求分派到目标虚拟主机。如果未正确验证该头部值，攻击者可以提供无效输入，导致 Web 服务器：

- 将请求分派到列表中的第一个虚拟主机。
- 执行重定向到攻击者控制的域。
- 执行 Web 缓存投毒。
- 操纵密码重置功能。
- 允许访问本不应从外部访问的虚拟主机。

## 测试目标

- 评估应用程序是否动态解析 Host 头。
- 绕过依赖该头部的安全控制。

## 如何测试

初始测试非常简单，只需在 Host 头字段中提供另一个域（例如 `attacker.com`）。影响取决于 Web 服务器如何处理该头部值。当 Web 服务器处理输入以将请求发送到位于所提供域的攻击者控制主机，而不是 Web 服务器上的内部虚拟主机时，攻击即有效。

```http
GET / HTTP/1.1
Host: www.attacker.com
[...]
```

在最简单的情况下，这可能导致 302 重定向到所提供的域。

```http
HTTP/1.1 302 Found
[...]
Location: https://www.attacker.com/login.php

```

或者，Web 服务器可能将请求发送到列表中的第一个虚拟主机。

### X-Forwarded-Host 头部绕过

如果通过检查 Host 头部中注入的无效输入来缓解 Host 头注入，则可以将该值提供给 `X-Forwarded-Host` 头部。

```http
GET / HTTP/1.1
Host: www.example.com
X-Forwarded-Host: www.attacker.com
[...]
```

可能产生如下的客户端输出：

```html
[...]
<link src="https://www.attacker.com/link" />
[...]
```

同样，这取决于 Web 服务器如何处理该头部值。

### Web 缓存投毒

使用此技术，攻击者可以操纵 Web 缓存，向任何请求者提供投毒内容。这依赖于能够投毒应用程序自身运行的缓存代理、CDN 或其他下游提供商。结果，受害者在请求易受攻击的应用程序时将无法控制是否接收到恶意内容。

```http
GET / HTTP/1.1
Host: www.attacker.com
[...]
```

当受害者访问易受攻击的应用程序时，以下内容将从 Web 缓存中提供。

```html
[...]
<link src="https://www.attacker.com/link" />
[...]
```

### 密码重置投毒

密码重置功能通常会在创建使用生成秘密令牌的密码重置链接时包含 Host 头值。如果应用程序处理攻击者控制的域来创建密码重置链接，受害者可能会点击电子邮件中的链接，从而允许攻击者获取重置令牌，进而重置受害者的密码。

以下示例显示了一个在 PHP 中使用 `$_SERVER['HTTP_HOST']` 值生成的密码重置链接，该值基于 HTTP Host 头的内容设置：

```php
$reset_url = "https://" . $_SERVER['HTTP_HOST'] . "/reset.php?token=" .$token;
send_reset_email($email,$rset_url);
```

通过使用篡改的 Host 头向密码重置页面发出 HTTP 请求，我们可以修改 URL 指向的位置：

```http
POST /request_password_reset.php HTTP/1.1
Host: www.attacker.com
[...]

email=user@example.org
```

指定的域（`www.attacker.com`）随后将被用于重置链接，该链接会通过电子邮件发送给用户。当用户点击此链接时，攻击者可以窃取令牌并危害其账户。

```text
... 邮件片段 ...

点击以下链接重置您的密码：

https://www.attacker.com/reset.php?token=12345

... 邮件片段 ...
```

### 访问私有虚拟主机

在某些情况下，服务器可能拥有不打算从外部访问的虚拟主机。这在使用[分离式 DNS](https://en.wikipedia.org/wiki/Split-horizon_DNS) 设置（其中内部和外部 DNS 服务器对同一域返回不同记录）时最常见。

例如，一个组织在其内部网络上可能只有一个 Web 服务器，同时托管其公共网站（在 `www.example.org`）和内部 Intranet（在 `intranet.example.org`，但该记录仅存在于内部 DNS 服务器上）。虽然无法从网络外部直接浏览到 `intranet.example.org`（因为该域无法解析），但可能通过从外部发送带有以下 `Host` 头的请求来访问 Intranet：

```http
Host: intranet.example.org
```

这也可以通过将 `intranet.example.org` 的条目添加到 hosts 文件中（使用 `www.example.org` 的公网 IP 地址）来实现，或者在测试工具中覆盖 DNS 解析。

## 参考资料

- [什么是 Host 头攻击？](https://www.acunetix.com/blog/articles/automated-detection-of-host-header-attacks/)
- [Host 头攻击](https://www.briskinfosec.com/blogs/blogsdetail/Host-Header-Attack)
- [HTTP Host 头攻击](https://portswigger.net/web-security/host-header)
