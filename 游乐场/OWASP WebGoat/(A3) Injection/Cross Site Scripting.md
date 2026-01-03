---
id: 
title: Cross Site Scripting
---
<!-- muse start -->

<!-- muse end -->

## 2. 什么是XSS？

跨站脚本攻击（简称XSS）是一种安全漏洞，其成因是允许将HTML/脚本标签作为输入内容，并在未经编码或过滤的情况下直接渲染到浏览器中。

### 跨站脚本攻击（XSS）是目前最普遍且危害性最大的Web应用程序安全问题

尽管针对此攻击存在简单且广为人知的防御方案，但互联网上仍存在大量相关案例。修复方案的覆盖范围也往往成为彻底解决该问题的难点。我们将在后续内容中详细讨论防御措施。

### XSS具有显著危害性

特别是随着"富互联网应用"日益普及，通过JavaScript连接的权限功能调用可能被破坏。若未得到充分保护，敏感数据（如身份验证Cookie）可能被窃取并用于他人目的。

快速示例：

- 通过浏览器（Chrome、Firefox）开发者工具中的JavaScript控制台执行：
    ```js
    alert("XSS测试");
    alert(document.cookie);
    ```
- 任何返回至客户端的数据字段均存在注入可能性
    ```js
    <script>alert("XSS测试")</script>
    ```

## 3. 最常见的位置

- 向用户回显搜索字符串的搜索字段
- 回显用户数据的输入字段
- 返回用户所提供文本的错误消息
- 包含用户所提供数据的隐藏字段
- 任何显示用户所提供数据的页面
  - 留言板
  - 自由格式评论
- HTTP头

## 4. 为何需要关注XSS？

### XSS攻击可能导致以下后果：

- 窃取会话Cookie
- 伪造请求
- 在页面创建虚假字段以收集凭据
- 将页面重定向至"恶意"网站
- 伪装成合法用户发起请求
- 窃取机密信息
- 在终端用户系统上执行恶意代码（活动脚本）
- 插入恶意及不当内容
    ```html
    <img src="http://malicious.site.com/image.jpg/>
    ">GoodYear recommends buying BridgeStone tires...
    ```

### XSS攻击增强钓鱼攻击的可信度

- URL中使用了合法域名

## 5. XSS类型

### 反射型

- 来自用户请求的恶意内容在网页浏览器中显示给用户
- 恶意内容在服务器响应后被写入页面
- 需要社会工程学手段配合
- 以浏览器中继承自用户的权限运行

### 基于DOM型（技术上亦属反射型）

- 客户端脚本使用来自用户请求的恶意内容向页面写入HTML
- 与反射型XSS类似
- 以浏览器中继承自用户的权限运行

### 存储型/持久型

- 恶意内容存储在服务器（数据库、文件系统或其他对象中），后续在网页浏览器中显示给用户
- 无需社会工程学手段配合

## 6. 反射型XSS攻击场景

- 攻击者向受害者发送恶意URL
- 受害者点击链接加载恶意网页
- 嵌入URL中的恶意脚本在受害者浏览器中执行
  - 脚本窃取敏感信息（如会话ID）并发送给攻击者
- 受害者未察觉攻击发生

![Web Goat Reflected-XSS](./images/Reflected-XSS.png)
*Web Goat Reflected-XSS*

## 7. 动手尝试！反射型XSS

本任务目标是识别哪个字段存在XSS漏洞。

在服务器端验证所有输入始终是良好实践。当未经验证的用户输入被用于HTTP响应时，就可能发生XSS攻击。在反射型XSS攻击中，攻击者可构造包含攻击脚本的URL，并将其发布到其他网站、通过邮件发送或诱使受害者点击。

检测字段是否存在XSS漏洞的简易方法是使用`alert()`或`console.log()`方法。请选用其中一种方法来定位存在漏洞的字段。

目标功能在点击购买按钮后反射行用卡号，且不限制为数字

输入经典向量得到弹框
```js
<script>alert("XSS")</script>
```

## 9. 反射型与基于DOM型的XSS

基于DOM型的XSS是反射型XSS的另一种形式。两者均通过向受害者发送包含可在浏览器中反射输入的链接来触发。DOM型与传统反射型XSS的区别在于，DOM型攻击中恶意载荷永远不会发送至服务器，仅由客户端进行处理。

-   攻击者向受害者发送恶意URL
-   受害者点击该链接
-   该链接可能加载一个恶意网页，或加载一个受害者正在使用（可能处于已登录状态）且存在漏洞的路由/处理程序的网页
-   若为恶意网页，其可能利用自身的JavaScript攻击另一个存在漏洞路由/处理程序的页面/URL
-   存在漏洞的页面渲染该恶意载荷，并在该页面/站点上以用户上下文权限执行攻击
-   攻击者的恶意脚本可能以本地账户权限执行命令

受害者未察觉攻击发生…恶意攻击者通常不会使用 `<script>alert('xss')</script>` 此类明显语句。

## 10. 识别基于DOM型XSS的潜在风险

基于DOM型XSS通常可通过检查客户端代码中的路由配置来发现。重点寻找接收输入参数并将其"反射"到页面的路由。

在此示例中，您需要关注路由处理程序中的某些"测试"代码（WebGoat使用backbone作为主要JavaScript库）。有时测试代码会遗留在生产环境中（且测试代码通常较为简单，缺乏安全性或质量控制！）。

您的目标是找到该路由并利用其漏洞。首先需要明确：基础路由是什么？以本课程URL为例，其格式应类似于`/WebGoat/start.mvc#lesson/CrossSiteScripting.lesson/9`。此处的"基础路由"为：`start.mvc#lesson/`，后续的`CrossSiteScripting.lesson/9`是由JavaScript路由处理程序处理的参数。

那么，在生产环境中遗留的测试代码对应路由是什么？要回答此问题，您需要检查JavaScript源代码。

此挑战仅为陈旧功能端点发现的信息收集，之后的挑战是对 DOM XSS 的源的处理器发现。

在浏览器开发者工具的查看器中搜索 `router`
定位路由脚本 `js/goatApp/view/GoatRouter.js`
在此脚本中找到对应路由代码
```js
routes: {
            'welcome': 'welcomeRoute',
            'lesson/:name': 'lessonRoute',
            'lesson/:name/:pageNum': 'lessonPageRoute',
            'test/:param': 'testRoute',
            'reportCard': 'reportCard'
        }
```

由示例的基础路由 `start.mvc#lesson` 构建为 `start.mvc#test`


## 11. 动手尝试！基于DOM型XSS

部分攻击属于"盲攻击"。幸运的是，您当前运行的服务器可提供反馈，便于确认攻击是否成功。请使用刚发现的路由，尝试通过未编码的路由参数反射来执行WebGoat内部函数。需要执行的函数为：

webgoat.customjs.phoneHome()

当然，您可以通过控制台/调试方式触发该函数，但此处要求通过新标签页的URL链接触发。

成功触发后，浏览器控制台将收到包含随机数的后续响应。请将该随机数填写至下方输入框。

基于 10. 挑战的已知路由与参数格式
尝试添加参数 `start.mvc#test/foo` 参数被反射

构建 URL，载荷使用 URL编码
`http://localhost:3000/WebGoat/start.mvc?username=apkallus#test/%3Cscript%3Ewebgoat.customjs.phoneHome%28%29%3C%2Fscript%3E`
打开控制台得到
`phone home said {"lessonCompleted":true,"feedback":"Congratulations. You have successfully completed the assignment.","feedbackArgs":null,"output":"phoneHome Response is -1065483869","outputArgs":null,"assignment":"DOMCrossSiteScripting","attemptWasMade":true}`

虽然使用反射型 XSS 探测通过挑战，但继续查找代码

路由设置 `lessonController.testHandler` 路由处理函数
`http://localhost:3000/WebGoat/js/goatApp/view/GoatRouter.js`
```js
testRoute: function (param) {
            this.lessonController.testHandler(param);
            //this.menuController.updateMenu(name);
        }
```

路由处理函数调用 `lessonContentView.showTestParam` 功能函数
`http://localhost:3000/WebGoat/js/goatApp/controller/LessonController.js`
```js
his.testHandler = function(param) {
    console.log('test handler');
    this.lessonContentView.showTestParam(param);
};
```

此处即为源的处理器，将参数以 HTML 格式显示。
`http://localhost:3000/WebGoat/js/goatApp/view/LessonContentView.js`
```js
/* for testing */
showTestParam: function (param) {
    this.$el.find('.lesson-content').html('test:' + param);
}
```