---
id: 
title: HTML tampering
---
<!-- muse start -->
Web Goat 对服务器使用客户端数据而不保存或验证的简略示例。
<!-- muse end -->

## 1. 概念

浏览器通常提供多种编辑显示内容的选项。因此，开发人员必须意识到，用户发送的值可能已被篡改。

## 2. 动手尝试

在一家在线商店，您订购了一台新电视，尝试以更低的价格购买一台或多台电视。

基准请求为
```http
POST /WebGoat/HtmlTampering/task HTTP/1.1
Host: localhost:3000

QTY=1&Total=2999.99
```
修改请求体的价格参数值通过挑战
`QTY=1&Total=0`

## 3. 缓解措施

在这个简单的示例中，您会注意到价格是在客户端计算并发送到服务器的。服务器接受了该输入值，并未重新计算价格。这种情况下的一个缓解措施是在您的数据库中查找电视的价格，并重新计算总价。

在实际应用中，永远不应依赖客户端验证。验证客户端发送的所有输入至关重要。请始终牢记：**永远不要信任客户端发送的输入**。

### 参考文献
https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
