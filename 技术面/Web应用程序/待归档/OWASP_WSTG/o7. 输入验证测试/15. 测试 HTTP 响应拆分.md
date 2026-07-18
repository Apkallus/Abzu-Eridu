# 测试 HTTP 响应拆分

|ID          |
|------------|
|WSTG-INPV-15|

## 概述

HTTP 响应拆分是一种漏洞，当应用程序将未经清理的用户输入放入 HTTP 响应头时，攻击者可以注入回车（CR）和换行（LF）字符。结果，单个 HTTP 响应可能被客户端或中间系统解释为多个不同的响应。

成功利用 HTTP 响应拆分漏洞可能导致各种影响，包括 Web 缓存投毒、跨站脚本（XSS）、内容欺骗、会话固定或其他客户端攻击，具体取决于注入的响应如何处理。

本节仅关注在应用层识别和测试 HTTP 响应拆分漏洞。HTTP 请求走私依赖于多个 HTTP 代理之间的解析不一致性，将在另一章节中讨论。

## 测试目标

- 识别被反射到 HTTP 响应头中的用户可控输入。
- 评估是否可以将 CR（`\r`）和 LF（`\n`）字符注入响应头。
- 确定成功的 HTTP 响应拆分攻击的潜在影响，例如缓存投毒或客户端利用。

## 如何测试

### 黑盒测试

某些 Web 应用程序使用用户提供的输入来生成某些 HTTP 响应头的值。一个常见的例子是重定向逻辑，其中目标 URL 来自请求参数。

例如，假设用户被要求在标准界面和高级界面之间进行选择。所选选项作为参数传递，并反映在重定向响应头中。

如果参数 `interface` 的值为 `advanced`，应用程序可能响应：

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 03 Dec 2005 16:22:19 GMT
Location: https://victim.com/main.jsp?interface=advanced
```

当浏览器收到此响应时，它会跟随 `Location` 头中指定的 URL。但是，如果应用程序未正确验证或清理用户输入，攻击者可能会注入序列 `%0d%0a`，即用于分隔 HTTP 头行的 CRLF 字符。

通过注入 CRLF 序列，测试人员可能导致下游客户端或中间系统（如 Web 缓存）将该响应解释为两个独立的 HTTP 响应。这种行为可被利用来投毒缓存或向用户传递恶意内容。

例如，测试人员为 `interface` 参数提供以下值：

`advanced%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0aContent-Length:%2035%0d%0a%0d%0a<html>Sorry,%20System%20Down</html>`

易受攻击的应用程序返回的响应可能为：

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 03 Dec 2005 16:22:19 GMT
Location: https://victim.com/main.jsp?interface=advanced
Content-Length: 0

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 35

<html>Sorry,%20System%20Down</html>
```

处理此响应的 Web 缓存可能将其解释为两个不同的响应。如果攻击者立即对 `/index.html` 发出后续请求，缓存可能会将该请求与第二个响应关联并存储。结果，后续所有通过该缓存访问 `victim.com/index.html` 的用户都可能收到攻击者控制的内容。

或者，攻击者可以注入 JavaScript 负载，对由被投毒缓存服务的用户发起跨站脚本攻击。虽然漏洞存在于应用程序中，但主要目标为其用户。

为识别此问题，测试人员应查找所有影响 HTTP 响应头的用户可控输入，并验证是否可以注入 CRLF 序列。

最常与 HTTP 响应拆分关联的响应头包括：

- `Location`
- `Set-Cookie`

在现实场景中成功利用可能需要仔细考虑其他因素：

- 测试人员可能需要构造适合缓存的响应头（例如，`Last-Modified` 设置为未来的日期），并可能使用 `Pragma: no-cache` 等头部使现有缓存条目失效。
- 应用程序可能过滤 CRLF 字符，但允许替代编码或字符表示，这有时可用于绕过输入验证。
- 某些平台会对响应头（如 `Location` 头中的路径）进行 URL 编码，但保留查询字符串不编码，从而允许通过 URL 的特定组件进行注入。

有关此类攻击的更深入讨论和其他利用场景，请参阅参考资料部分中列出的白皮书。

### 灰盒测试

在灰盒测试场景中，对应用程序架构和服务器行为的了解可提高利用的可靠性。

不同的服务器或中介可能以不同方式确定消息边界（例如，使用固定大小的缓冲区），需要精确的偏移量或填充。当易受攻击的参数通过 GET 传输时，URL 长度限制可能会截断负载。测试人员应识别替代注入点或请求方法（例如 POST），以更好地控制负载长度和位置。

## 修复

确保用户提供的输入在放入 HTTP 头之前经过严格的验证和清理。

- **输入验证：** 在将包含回车（`\r`、`%0d`）或换行（`\n`、`%0a`）字符的输入用于 HTTP 头之前，拒绝或剥离这些字符。
- **URL 编码：** 如果输入是 URL 的一部分（例如在 `Location` 头中），确保进行适当的 URL 编码，以防止控制字符被解释为分隔符。
- **使用安全框架：** 使用内置框架函数（如 `setHeader()`、`addHeader()`）设置头，而不是手动构造原始 HTTP 响应字符串。现代环境通常默认阻止头部注入。

## 工具

- [ZAP](https://www.zaproxy.org/)
- [Burp Suite](https://portswigger.net/burp)
- [CRLFuzz](https://github.com/dwisiswant0/crlfuzz) - 专为扫描 CRLF 漏洞而设计的工具。
- [Nuclei](https://github.com/projectdiscovery/nuclei) - 可与特定模板一起使用以检测 CRLF 注入模式。

## 参考资料

- [Amit Klein, “分而治之：HTTP 响应拆分、Web 缓存投毒攻击及相关主题”](https://packetstormsecurity.com/files/32815/Divide-and-Conquer-HTTP-Response-Splitting-Whitepaper.html)
- [Amit Klein: “HTTP 消息拆分、走私及其他”](https://www.slideserve.com/alicia/http-message-splitting-smuggling-and-other-animals-powerpoint-ppt-presentation)
- [Amit Klein: “HTTP 请求走私 - 勘误（IIS 48K 缓冲区现象）”](https://web.archive.org/web/20210614052317/https://www.securityfocus.com/archive/1/411418)
- [Amit Klein: “HTTP 响应走私”](https://web.archive.org/web/20210126213458/https://www.securityfocus.com/archive/1/425593)
- [Chaim Linhart, Amit Klein, Ronen Heled, Steve Orrin: “HTTP 请求走私”](https://web.archive.org/web/20210816212852/https://www.cgisecurity.com/lib/http-request-smuggling.pdf)
