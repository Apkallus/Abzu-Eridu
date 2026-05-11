---
title: Email Leak
description: 若响应的跨域头部使用通配符，那么可能存在 JSONP 方式的跨域数据传送。对 URL 参数进行探测，确认响应是否为 JSONP 的回调函数。移除自定义或无法控制或预测的 URL 参数或头部，确认敏感数据是否仅使用 Cookie 头部验证。若 JSONP 仅使用 Cookie 或可预测与控制的内容返回敏感数据，则存在跨域漏洞。即对于敏感数据响应，查看同源头部、检查回调参数、检查验证方式
---

- 描述：通过跨域访问数据，执行非意愿的信息披露。

- ```Access-Control-Allow-Origin: *```
    > 对于不包含凭据的请求，服务器会以“*”作为通配符，从而允许任意来源的请求代码都具有访问资源的权限。尝试使用通配符来响应包含凭据的请求会导致错误。[^MDN]

- JSONP
    > 粗略的JSONP部署很容易受到跨站请求伪造（CSRF/XSRF）的攻击[1]。因为HTML ```<script>``` 标签在浏览器里不遵守同源策略，恶意网页可以要求并获取属于其他网站的JSON资料。[^wiki]

- 提示：这个挑战使用了一种早已不再推荐的老方法。
    - callback

- 查看示例解决方案
    - 在端点 ```/rest/user/whoami```
        > 即使移除"Authorization"头它仍然能工作
        添加一个名为"callback"的 URL 参数。这将导致 API 将内容作为 JavaScript 片段（JSONP）返回，而不仅仅是标准的 JSON 对象。
    

[^MDN]: https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin

[^wiki]: https://zh.wikipedia.org/zh-cn/JSONP