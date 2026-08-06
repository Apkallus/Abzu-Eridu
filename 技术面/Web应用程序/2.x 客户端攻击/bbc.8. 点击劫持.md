# 第8章：点击劫持（Clickjacking）

点击劫持（或称用户界面伪装）是一种攻击，通过将恶意按钮伪装成合法按钮来诱骗用户点击。攻击者利用 HTML 页面叠加技术，将一个网页隐藏在另一个网页内部来实现此目的。让我们讨论这个有趣的可利用漏洞，为什么它是个问题，以及如何发现它的实例。

请注意，点击劫持在漏洞赏金计划中很少被视为有效范围，因为它通常涉及大量受害者端的用户交互。许多计划明确将点击劫持列为范围外，因此在开始寻找之前，请务必检查计划的政策！不过，如果你能证明点击劫持漏洞的影响，某些计划仍然会接受它。我们将在本章后面看到一个被接受的报告示例。

## 机制

点击劫持依赖于一种名为 iframe 的 HTML 特性。HTML iframe 允许开发人员通过将 `<iframe>` 标签放置在页面上，然后在标签的 `src` 属性中指定要嵌入的 URL，从而将一个网页嵌入另一个网页中。例如，将以下页面保存为 HTML 文件并用浏览器打开：

```html
<html>
<h3>This is my web page.</h3>
<iframe src="https://www.example.com" width="500" height="500"></iframe>
<p>If this window is not blank, the iframe source URL can be framed!</p>
</html>
```

你应该会看到一个类似于图 8-1 的网页。注意一个框中将 `www.example.com` 放置在主页面的一片区域中。

*（图 8-1：如果 iframe 不为空，则 iframe 的 src 属性中指定的页面可以被嵌入！）*

有些网页无法被嵌入。如果你将无法被嵌入的页面放入 iframe，你应该会看到一个空白的 iframe，如图 8-2 所示。

*（图 8-2：如果 iframe 为空，则 iframe 源无法被嵌入。）*

iframe 在很多方面都很有用。你常在网页顶部或侧面看到的在线广告就是 iframe 的例子；公司利用它们将预先制作好的广告包含在你的社交媒体或博客中。iframe 还允许你在网页中嵌入其他互联网资源，如视频和音频。例如，这个 iframe 允许你在外部站点中嵌入 YouTube 视频：

```html
<iframe width="560" height="315"
src="https://www.youtube.com/embed/d1192Sqk" frameborder="0"
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen>
</iframe>
```

iframe 使我们的互联网变得更加生动和互动。但它们也可能对被嵌入的网页构成危险，因为它们引入了点击劫持攻击的可能性。假设 example.com 是一个银行站点，包含一个点击按钮即可转账的页面。你可以通过 URL `https://www.example.com/transfer_money` 访问转账页面。

该 URL 接受两个参数：收款人账户 ID 和转账金额。如果你使用这些参数访问 URL，例如 `https://www.example.com/transfer_money?recipient=RECIPIENT_ACCOUNT&amount=AMOUNT_TO_TRANSFER`，页面上的 HTML 表单将显示为已预填（图 8-3）。你只需点击 Submit 按钮，HTML 表单就会发起转账请求。

*（图 8-3：带有预填 HTTP POST 参数的转账页面）*

现在想象一下，攻击者将这个敏感的银行页面嵌入自己站点的一个 iframe 中，如下所示：

```html
<html>
<h3>Welcome to my site!</h3>
<iframe src="https://www.example.com/transfer_money?recipient=attacker_account_12345&amount=5000"
width="500" height="500">
</iframe>
</html>
```

这个 iframe 嵌入了转账页面的 URL，并通过 URL 参数预填了收款人和金额。攻击者将这个 iframe 隐藏在一个看似无害的网站上，然后诱骗用户点击敏感页面上的按钮。为了达到这个目的，他们以遮蔽银行表单的方式叠加多个 HTML 元素。以这个 HTML 页面为例：

```html
<html>
<style>
#victim-site {
  width:500px;
  height:500px;
  ① opacity:0.00001;
  ② z-index:1;
}
#decoy {
  ③ position:absolute;
  width:500px;
  height:500px;
  ④ z-index:-1;
}
</style>
<div id="decoy">
  <h3>Welcome to my site!</h3>
  <h3>This is a cybersecurity newsletter that focuses on bug
  bounty news and write-ups!
  Please subscribe to my newsletter below to receive new
  cybersecurity articles in your email inbox!</h3>
  <form action="/subscribe" method="post">
    <label for="email">Email:</label>
    ⑤ <br>
    <input type="text" id="email" value="Please enter your email!">
    ⑥ <br><br>
    <input type="submit" value="Submit">
  </form>
</div>
<iframe id="victim-site"
src="https://www.example.com/transfer_money?recipient=attacker_account_12345&amount=5000"
width="500" height="500">
</iframe>
</html>
```

你可以看到我们在 HTML 页面顶部添加了 `<style>` 标签。`<style>` 标签之间的内容是 CSS 代码，用于指定 HTML 元素的样式，如字体颜色、元素大小和透明度。我们可以通过为 HTML 元素分配 ID 并在样式表中引用它们来设置样式。

这里，我们将诱饵元素的位置设置为 `absolute`，使诱饵站点与包含受害者站点的 iframe 重叠 ③。如果没有绝对定位指令，HTML 会在屏幕的不同部分显示这些元素。诱饵元素包含一个 “订阅新闻通讯” 按钮，我们通过 HTML 的换行标签 `<br>` ⑤⑥ 产生的新行仔细定位 iframe，使 “转账” 按钮正好位于 “订阅” 按钮之上。然后我们通过将 iframe 的透明度设置为一个非常低的值 ① 使其不可见。最后，我们将 iframe 的 `z-index` 设置为比诱饵更高的值 ②④。`z-index` 设置不同 HTML 元素的堆叠顺序。如果两个 HTML 元素重叠，`z-index` 最高的将位于顶部。

通过为受害者站点 iframe 和诱饵表单设置这些 CSS 属性，我们得到了一个看似订阅新闻通讯的页面，但实际上包含一个不可见的表单，会将用户的钱转入攻击者的账户。

让我们将 iframe 的透明度调回 `opacity:1` 来看看页面实际布局。你可以看到 “转账” 按钮正好位于 “订阅新闻通讯” 按钮的正上方（图 8-4）。

*（图 8-4：“转账” 按钮正好位于 “订阅” 按钮之上。受害者以为自己正在订阅新闻通讯，实际上点击的是授权转账的按钮。）*

一旦我们将 iframe 的透明度重置为 `opacity:0.00001` 使敏感表单不可见，该站点看起来就像普通的新闻通讯页面（图 8-5）。

*（图 8-5：攻击者通过使敏感表单不可见来诱骗用户点击按钮。）*

如果用户已登录银行站点，他们也会在 iframe 中处于登录状态，因此银行站点的服务器会将 iframe 发送的请求视为合法。当用户点击看似无害的按钮时，他们实际上在 example.com 上执行了转账！他们意外地将 5,000 美元从银行账户余额转入了攻击者的账户，而不是订阅新闻通讯。这就是为什么我们将这种攻击称为用户界面伪装或点击劫持：攻击者伪装用户界面来劫持用户点击，将本应用于其页面的点击重新用于受害者站点。

这是一个简化示例。实际上，支付应用程序不会以这种方式实现，因为那会违反数据安全标准。另外要记住的是，在关键功能上存在容易预防的漏洞（如转账页面上的点击劫持漏洞）表明该应用程序未遵循安全开发的最佳实践。这个示例应用程序很可能包含其他漏洞，你应该对其进行全面测试。

## 防御措施

点击劫持漏洞的发生需要满足两个条件。首先，易受攻击的页面必须具有代表用户执行状态更改操作的功能。状态更改操作会以某种方式更改用户账户，例如更改用户账户设置或个人数据。其次，易受攻击的页面必须允许自己被另一个站点上的 iframe 嵌入。

HTTP 响应头 `X-Frame-Options` 允许网页指示页面内容是否可以在 iframe 中渲染。浏览器将遵循所提供的头指令。否则，页面默认是可被嵌入的。

该头提供两个选项：`DENY` 和 `SAMEORIGIN`。如果页面带有 `DENY` 选项，则完全不能被嵌入。`SAMEORIGIN` 选项允许来自同源（即具有相同协议、主机和端口的页面）的页面进行嵌入。

```
X-Frame-Options: DENY
X-Frame-Options: SAMEORIGIN
```

为防止敏感操作上的点击劫持，站点应在所有包含状态更改操作的页面上提供这些选项之一。

`Content-Security-Policy` 响应头是另一种可能的点击劫持防御手段。该头的 `frame-ancestors` 指令允许站点指示页面是否可以被嵌入。例如，将该指令设置为 `'none'` 将阻止任何站点嵌入该页面，而设置为 `'self'` 则允许当前站点嵌入该页面：

```
Content-Security-Policy: frame-ancestors 'none';
Content-Security-Policy: frame-ancestors 'self';
```

将 `frame-ancestors` 设置为特定源将允许该源嵌入内容。以下头将允许当前站点以及 example.com 子域上的任何页面嵌入其内容：

```
Content-Security-Policy: frame-ancestors 'self' *.example.com;
```

除了实施 `X-Frame-Options` 和 `Content-Security-Policy` 以确保敏感页面无法被嵌入之外，另一种防止点击劫持的方法是使用 SameSite Cookie。Web 应用程序通过 `Set-Cookie` 头指示用户浏览器设置 Cookie。例如，以下头将使客户端浏览器将 Cookie `PHPSESSID` 的值设置为 `UEhQU0VTU0lE`：

```
Set-Cookie: PHPSESSID=UEhQU0VTU0lE
```

除了基本的 `cookie_name=cookie_value` 指定之外，`Set-Cookie` 头还允许使用几个可选标志来保护用户的 Cookie。其中之一是 `SameSite` 标志，它有助于防止点击劫持攻击。当 Cookie 上的 `SameSite` 标志设置为 `Strict` 或 `Lax` 时，该 Cookie 不会在第三方 iframe 内发出的请求中发送：

```
Set-Cookie: PHPSESSID=UEhQU0VTU0lE; Max-Age=86400; Secure; HttpOnly; SameSite=Strict
Set-Cookie: PHPSESSID=UEhQU0VTU0lE; Max-Age=86400; Secure; HttpOnly; SameSite=Lax
```

这意味着任何需要受害者已认证的点击劫持攻击（如我们之前提到的银行示例）都不会成功，即使没有 HTTP 响应头限制嵌入，因为受害者在被劫持的请求中不会处于已认证状态。

## 寻找点击劫持

通过查找目标站点上包含敏感状态更改操作且可被嵌入的页面来发现点击劫持漏洞。

### 第 1 步：寻找状态更改操作

只有当目标页面包含状态更改操作时，点击劫持漏洞才有价值。你应该查找允许用户对其账户进行更改的页面，例如更改账户详细信息或设置。否则，即使攻击者能够劫持用户点击，也无法对网站或用户账户造成任何损害。因此，你应该首先识别站点上的状态更改操作。

例如，假设你正在测试 example.com 的一个子域，该子域在 `bank.example.com` 处理银行功能。遍历 Web 应用程序的所有功能，点击所有链接，并记录所有状态更改选项及其所在页面的 URL：

**bank.example.com 上的状态更改请求**
- 更改密码：`bank.example.com/password_change`
- 转账：`bank.example.com/transfer_money`
- 解除外部账户关联：`bank.example.com/unlink`

你还应该确认该操作是否仅通过点击即可完成。点击劫持只能伪造用户的点击，而无法伪造键盘操作。需要用户明确输入值的攻击虽然可能，但由于需要大量社会工程学，通常不可行。例如，在此银行页面上，如果应用程序要求用户明确输入收款人账户和转账金额，而不是从 URL 参数加载，那么通过点击劫持攻击它将不可行。

### 第 2 步：检查响应头

然后逐一检查你发现的每个状态更改功能，重新访问包含它们的页面。打开代理工具，拦截包含该网页的 HTTP 响应。查看页面是否带有 `X-Frame-Options` 或 `Content-Security-Policy` 头。

如果页面未带有任何这些头，则可能容易受到点击劫持攻击。如果状态更改操作要求用户在执行时已登录，你还应检查站点是否使用了 SameSite Cookie。如果使用了，你将无法在需要认证的站点功能上利用点击劫持攻击。

虽然设置 HTTP 响应头是防止这些攻击的最佳方法，但网站可能实施了其他不太明显的防护措施。例如，一种称为 **frame-busting** 的技术使用 JavaScript 代码检查页面是否在 iframe 中，以及是否被可信站点嵌入。Frame-busting 是一种不可靠的防点击劫持方法。事实上，frame-busting 技术通常可以被绕过，我将在本章后面演示。

你可以通过创建一个嵌入目标页面的 HTML 页面来确认页面是否可被嵌入。如果目标页面显示在框架中，则该页面是可嵌入的。以下 HTML 代码是一个很好的模板：

```html
<HTML>
<head>
<title>Clickjack test page</title>
</head>
<body>
<p>Web page is vulnerable to clickjacking if the iframe is populated with the target page!</p>
<iframe src="URL_OF_TARGET_PAGE" width="500" height="500"></iframe>
</body>
</html>
```

### 第 3 步：确认漏洞

通过在你的测试账户上执行点击劫持攻击来确认漏洞。你应该尝试通过刚刚构造的框架页面执行状态更改操作，并查看操作是否成功。如果你能仅通过点击经由 iframe 触发该操作，则该操作容易受到点击劫持攻击。

## 绕过防护

当站点实施了适当的防护措施时，点击劫持就无法实现。如果现代浏览器显示受 `X-Frame-Options` 保护的页面，那么你很可能无法在该页面上利用点击劫持，只能寻找其他漏洞（如 XSS 或 CSRF）来达到相同目的。但有时，即使页面缺少防止点击劫持的头，它也不会出现在你的测试 iframe 中。如果网站本身未能实施完整的点击劫持防护，你可能可以绕过这些缓解措施。

如果网站使用 frame-busting 技术而非 HTTP 响应头和 SameSite Cookie，你可以尝试以下方法：在 frame-busting 代码中寻找漏洞。例如，开发人员常犯的一个错误是在检测受保护页面是否被恶意页面嵌入时，只比较顶层框架与当前框架。如果顶层框架与嵌入页面同源，开发人员可能会允许它，因为他们认为嵌入站点的域是安全的。本质上，防护代码具有以下结构：

```javascript
if (top.location == self.location) {
  // 允许嵌入。
} else {
  // 禁止嵌入。
}
```

如果是这种情况，请在受害者站点上寻找允许你嵌入自定义 iframe 的位置。例如，许多社交媒体站点允许用户在其个人资料上分享链接。这些功能通常通过将 URL 嵌入 iframe 来显示信息和链接缩略图。其他需要自定义 iframe 的常见功能包括允许嵌入视频、音频、图片、自定义广告和网页构建器的功能。

如果你找到这些功能之一，你可能可以通过 **双重 iframe 技巧** 绕过点击劫持防护。该技巧通过将你的恶意页面嵌入受害者域内的一个页面中来工作。首先，构造一个嵌入受害者目标功能的页面。然后将整个页面放入受害者站点托管的 iframe 中（图 8-6）。

*（图 8-6：你可以尝试将你的站点放入受害者站点托管的 iframe 中，以绕过不完善的框架检查。）*

这样，`top.location` 和 `self.location` 都指向 `victim.com`。frame-busting 代码会确定最内层的 victim.com 页面被其域内的另一个 victim.com 页面嵌入，因此认为嵌入是安全的。中间的攻击者页面将不会被检测到。

始终问自己，开发人员在实施保护机制时是否可能遗漏了任何边缘情况。你能利用这些边缘情况为自己谋利吗？

让我们看一个示例报告。Periscope 是一个直播视频应用程序，在 2019 年 7 月 10 日被发现存在点击劫持漏洞。你可以在 https://hackerone.com/reports/591432/ 找到已披露的漏洞报告。该站点使用 `X-Frame-Options ALLOW-FROM` 指令来防止点击劫持。此指令允许页面指定允许嵌入它的 URL，但它是一个已废弃的指令，许多浏览器不支持它。这意味着如果受害者使用不支持该指令的浏览器（如最新的 Chrome、Firefox 和 Safari 浏览器），子域 `https://canary-web.pscp.tv` 和 `https://canary-web.periscope.tv` 上的所有功能都容易受到点击劫持攻击。由于 Periscope 的账户设置页面允许用户停用其账户，攻击者可以嵌入设置页面并诱骗用户停用其账户。

## 提升攻击影响

网站经常在没有点击劫持防护的情况下提供页面。只要页面不包含可利用的操作，缺少点击劫持防护就不被视为漏洞。另一方面，如果可嵌入页面包含敏感操作，则点击劫持的影响将相应严重。

专注于应用程序最关键的功能以实现最大的业务影响。例如，假设一个站点有两个可嵌入页面。第一个页面包含一个执行用户银行余额转账的按钮，而第二个页面包含一个更改网站主题颜色的按钮。虽然这两个页面都存在点击劫持漏洞，但第一个页面上的点击劫持漏洞影响显著高于第二个。

你还可以组合多个点击劫持漏洞或将点击劫持与其他漏洞链接起来，为更严重的安全问题铺路。例如，应用程序通常根据用户偏好发送或披露信息。如果你能通过点击劫持更改这些设置，通常可以诱导敏感信息泄露。假设 `bank.example.com` 包含多个点击劫持漏洞。其中一个允许攻击者更改账户的账单邮箱，另一个允许攻击者将账户摘要发送到其账单邮箱。恶意页面的 HTML 如下所示：

```html
<html>
<h3>Welcome to my site!</h3>
<iframe src="https://bank.example.com/change_billing_email?email=attacker@attacker.com"
width="500" height="500">
</iframe>
<iframe src="https://bank.example.com/send_summary" width="500" height="500">
</iframe>
</html>
```

你可以首先将受害者的账单邮箱更改为你自己的邮箱，然后让受害者将账户摘要发送到你的邮箱，从而泄露账户摘要报告中包含的信息。根据账户摘要披露的内容，你可能能够收集与该账户关联的街道地址、电话号码和信用卡信息！请注意，要使此攻击成功，受害者用户需要点击攻击者站点两次。

### 关于交付点击劫持载荷的说明

在漏洞赏金报告中，你通常需要向公司展示真实攻击者可以有效利用你发现的漏洞。这意味着你需要了解攻击者如何在现实中利用点击劫持漏洞。

点击劫持漏洞依赖于用户交互。要使攻击成功，攻击者必须构造一个足够有说服力的站点让用户点击。这通常并不困难，因为用户在点击网页之前通常不会采取预防措施。但如果你想让攻击更具说服力，可以查看 Social-Engineer Toolkit（https://github.com/trustedsec/social-engineer-toolkit/）。这套工具可以帮助你克隆知名网站并将其用于恶意目的。然后你可以将 iframe 放置在克隆的网站上。

根据我的经验，放置隐藏按钮最有效的位置是直接位于 “请接受本网站使用 Cookie！” 弹窗之上。用户通常会在没有太多思考的情况下点击此按钮以关闭窗口。

## 找到你的第一个点击劫持漏洞！

现在你知道了点击劫持漏洞是什么、如何利用以及如何提升影响，去寻找你的第一个点击劫持漏洞吧！按照本章描述的步骤：

1. **识别网站上的状态更改操作**，并记录它们的 URL 位置。标记那些仅需鼠标点击即可执行的操作以供进一步测试。
2. **检查这些页面是否存在 `X-Frame-Options`、`Content-Security-Policy` 头以及 SameSite 会话 Cookie**。如果你找不到这些保护特性，该页面可能存在漏洞！
3. **构造一个嵌入目标页面的 HTML 页面**，并在浏览器中加载以查看页面是否被嵌入。
4. **通过在你的测试账户上执行模拟点击劫持攻击来确认漏洞**。
5. **设计一种巧妙的方式将载荷交付给最终用户**，并考虑漏洞的更广泛影响。
6. **起草你的第一份点击劫持报告！**