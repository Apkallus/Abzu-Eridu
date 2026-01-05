---
id: 
title: Bypass front-end restrictions
---
<!-- muse start -->
Web Goat 对绕过前端限制的简略示例。
<!-- muse end -->

## 1. 概念

用户对 Web 应用程序的前端拥有很大的控制权。他们可以修改 HTML 代码，有时也可以修改脚本。要求特定输入格式的应用程序也应该在服务器端进行验证。

## 2. 字段限制

在大多数浏览器中，客户端对网页的 HTML 部分拥有完全或几乎完全的控制权。他们可以更改值或限制以满足自己的偏好。

任务
发送一个绕过这五个字段所有限制的请求。

基准请求为
```http
POST /WebGoat/BypassRestrictions/FieldRestrictions HTTP/1.1
Host: localhost:3000

select=option1&radio=option1&checkbox=on&shortInput=12345&readOnlyInput=change
```

在拦截代理服务器中修改字段后通过挑战
`select=fooooooooooo&radio=fooooooooooo&checkbox=fooooooooooo&shortInput=fooooooooooo&readOnlyInput=fooooooooooo`

## 3. 验证

通常会有一些机制来防止用户向服务器发送经过修改的字段值，例如在发送前进行验证。Chrome 等大多数流行的浏览器不允许在运行时编辑脚本。我们必须通过其他方式来规避验证。

任务
发送一个不符合上述所有字段正则表达式的请求。

基准请求为
```http
POST /WebGoat/BypassRestrictions/frontendValidation HTTP/1.1
Host: localhost:3000

field1=abc&field2=123&field3=abc+123+ABC&field4=seven&field5=01101&field6=90210-1111&field7=301-604-4882&error=0
```
根据描述，修改字段3为字母、数字、空格外的其他字符，修改字段4为数字，而最后的隐藏参数`error`被客户端用来标识是否符合格式
`field1=fooooooooooo&field2=fooooooooooo&field3=''''''''&field4=12345678&field5=fooooooooooo&field6=fooooooooooo&field7=fooooooooooo&error=0`