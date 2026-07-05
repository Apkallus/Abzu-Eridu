## 空字节
### SOP 绕过——CVE-2007-0981

让我们来看一个由于层不匹配导致的 SOP 绕过的经典案例，该漏洞在 Firefox 旧版本中被发现，记录为 CVE-2007-0981。我们来看一下 POC：

```javascript
location.hostname = "evil.com\x00www.bing.com"
```

在此 POC 中，`location.hostname` 属性被设置为 `evil.com`，后跟一个空字节 `\x00`，然后是 `bing.com`。空字节在许多编程语言中被普遍视为字符串终止符。然而，在此情况下，DOM（渲染引擎的一部分）不将 `\x00` 视为字符串终止符。因此，它将 `evil.com\x00www.bing.com` 解释为 `bing.com` 的子域。



相反，DNS 解析器（网络层的一部分）确实将空字节识别为字符串终止符，并停止执行，将源视为 `evil.com`，忽略字符串的其余部分。因此，这将允许攻击者设置、更改或删除 `bing.com` 及其子域的 Cookie。

### SOP 绕过——CVE-2011–3246

CVE-2011–3246 是一个类似示例，影响 Safari 浏览器的旧版本。SOP 绕过又是逻辑混淆和层不匹配的非常类似的情况。然而，这次不匹配发生在持久层中的 Cookie 存储部分和网络层中的 DNS 解析器之间。

**POC**

```html
<img src="https://evil.com%00.bing.com">
```