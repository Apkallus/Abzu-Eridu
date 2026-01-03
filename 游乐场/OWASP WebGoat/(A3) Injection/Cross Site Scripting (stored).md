---
id: 
title: Cross Site Scripting (stored)
---
<!-- muse start -->
Web Goat 简化的储存型 XSS 示例
<!-- muse end -->

## 2. 存储型XSS

存储型跨站脚本攻击的不同之处在于，恶意载荷会被持久化存储（而非通过链接传递/注入）。

### 存储型XSS攻击场景

- 攻击者向留言板发布恶意脚本
- 消息被存储在服务器数据库中
- 受害者阅读该消息
- 嵌入在留言板帖子中的恶意脚本在受害者浏览器中执行
  - 脚本窃取会话ID等敏感信息并发送给攻击者
- 受害者未能察觉攻击发生

## 3. 查看以下注释内容

添加包含JavaScript载荷的注释。再次强调...您需要调用`webgoat.customjs.phoneHome`函数。

作为攻击者（攻防安全领域），请注意大多数应用程序不会存在如此直接命名的漏洞利用点。此外，您可能需要通过动态加载JavaScript的方式来完全实现数据提取目标。

通过浏览器开发者工具或代理工具观察，输出内容应包含以"phoneHome Response is..."开头的返回值。请将该数值填入下方以完成本练习。请注意，每次调用`phoneHome`方法都会改变该返回值，您可能需要确保获取的是最新数值。

在评论中输入载荷后
```html
<script>webgoat.customjs.phoneHome()</script>
```
打开控制台
`phone home said {"lessonCompleted":true,"feedback":"Congratulations. You have successfully completed the assignment.","feedbackArgs":null,"output":"phoneHome Response is -1760222390","outputArgs":null,"assignment":"DOMCrossSiteScripting","attemptWasMade":true}`