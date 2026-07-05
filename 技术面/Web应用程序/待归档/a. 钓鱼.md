

## 地址栏欺骗漏洞

根据 Google 的规则（[https://bughunters.google.com/about/rules/6625378258649088/google-and-alphabet-vulnerability-reward-program-vrp-rules](https://bughunters.google.com/about/rules/6625378258649088/google-and-alphabet-vulnerability-reward-program-vrp-rules)），地址栏是现代浏览器中唯一可以信赖的安全指示器。这似乎合乎逻辑，因为地址栏是用户确认自己是否在正确网站上的主要方式。

浏览器厂商意识到这一点，因此实施了内置控制，以确保浏览器中显示的内容与地址栏中的 URL 对应。

地址栏欺骗漏洞发生在地址栏指向用户试图访问的正确域，但该域的内容由攻击者控制时。在底层，基于浏览器的欺骗漏洞是通过利用浏览器中的缺陷来执行的，以制造用户正在合法域上的错觉。让我们看几个示例：

### 地址栏欺骗——新标签句柄控制

在 JavaScript 中，有几个函数允许用户延迟执行事件或以固定间隔执行事件。这些方法功能强大，可用于寻找地址栏欺骗漏洞。让我们看这种技术的一个示例：

**代码**

```html
<script>
w = window.open("www.facebook.com", "_blank");
setTimeout(function(){ w.document.write("<html>This is not Facebook</html>") }, 5000);
</script>
```

此脚本使用 `window.open` 函数在新窗口中打开 Facebook 网站，然后尝试在延迟五秒后使用 `document.write` 将页面内容覆盖为文本“This is not Facebook”。执行通过 `setTimeout` 函数延迟。在此过程中，浏览器可能无法更新地址栏，因此当地址栏仍然指向 `facebook.com` 时，实际显示的内容却由攻击者控制。以下是 Yandex 浏览器（CVE-2020–7369）使用相同技术保留地址栏的示例。

### 地址栏欺骗——持续刷新无效端口请求

触发地址栏欺骗的另一种技术是使用不存在的端口来保留地址栏，同时使用 JavaScript 定时函数诱导适当延迟。让我们看这种技术的一个示例：

**代码**

```html
<script>
function spoof() {
    document.write("<h1>This is not Bing</h1>");
    document.location = "https://bing.com:1234";
    setInterval(function(){ document.location = "https://bing.com:1234"; }, 9800);
};
</script>
```

该脚本使用 `document.location` 函数将用户重定向到非标准端口“1234”上的 `https://bing.com`。根据浏览器的不同，由于此端口上没有服务运行，最终返回连接超时错误之前会花费一些时间。在此时间段内，当浏览器尝试加载 `https://bing.com:1234` 时，`setInterval` 函数被重复调用，导致再次重定向到该 URL，从而在定义的时间间隔内重复该过程。

此过程在地址栏中保留欺骗的 URL，同时允许攻击者修改网页内容。这将在每次间隔后触发，从而在过程中保留 URL，同时允许攻击者向文档写入内容，导致地址栏欺骗。理想情况下，浏览器的正确行为是在 `setInterval` 函数被调用进行重定向时，重定向到“about:blank”。

相同的 POC 已被多次用于在 Safari 浏览器以及其他流行浏览器（如 Microsoft Edge 和 DuckDuckGo）中触发地址栏欺骗漏洞。有趣的是，Safari 浏览器会隐藏端口，因此用户唯一可见的 URL 是 `bing.com`。