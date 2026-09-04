文档
- [MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)

## HTTP 标头

### X-Frame-Options 点击劫持防护

用来给浏览器指示允许一个页面可否在 `<frame>`、`<iframe>`、`<embed>` 或者 `<object>` 中展现的标记。


### Content-Security-Policy (CSP) 内容安全策略

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/Content-Security-Policy

导航指令
- `frame-ancestors` 点击劫持防护
    指定可能嵌入页面的有效父项 `<frame>`、`<iframe>`、`<object>` 或 `<embed>`。

    - `frame-ancestors 'none'` 指令的行为类似于 X-Frame-Options 的 `deny` 指令。
    - `frame-ancestors 'self'` 指令大致等同于 X-Frame-Options 的 `sameorigin` 指令。


### Set-Cookie —— 将 cookie 由服务器发送到用户代理

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/Set-Cookie

