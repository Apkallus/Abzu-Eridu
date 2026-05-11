---
title: Unsigned JWT
description: 使用 none 签名的 JWT
---

- 描述：伪造一个本质上未签名的JWT令牌，该令牌冒充（不存在的）用户```jwtn3d@juice-sh.op```。
- 提示：获取应用程序用于其 JWT 的公共 RSA 密钥对此挑战是必须的。
    :x: 提示错误，此处仅使用 ```none``` 签名

- 使用 ```none``` 签名
    - 在 ```http://127.0.0.1:3000/profile``` 路径修改 cookie token 虽然不报错且能够设置字段。然而无法通过挑战
    - 在 查看示例解决方案，此挑战需在拥有 Authorization 头部的页面，修改此头部字段的 JWT 值
    - 访问 ```/rest/user/whoami``` ，使用 ```none```签名后通过挑战
