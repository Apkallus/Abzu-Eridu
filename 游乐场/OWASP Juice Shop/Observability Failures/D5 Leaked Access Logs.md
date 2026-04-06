---
title: Leaked Access Logs
description: 在访问日志的 URL 中寻找暴露的 URL 参数
---

- 描述：在互联网上翻垃圾箱寻找泄露的密码，并登录该密码所属的原用户账户。（用相同的密码创建新账户并不算作解决方案。）
- 查看示例解决方案
    1. 在 stackoverflow 平台查找拥有 ```access-log``` 标签的帖子
        https://stackoverflow.com/questions/tagged/access-log
    2. 根据对应 juice shop URL 的描述定位到帖子
        https://stackoverflow.com/questions/57061271/less-verbose-access-logs-using-expressjs-morgan
    3. 访问此帖子的详细日志链接 
        https://pastebin.com/4U1V1UjU
    4. 发现感兴趣的内容
        ```161.194.17.103 - - [27/Jan/2019:11:18:35 +0000] "GET /rest/user/change-password?current=0Y8rMnww$*9VFYE%C2%A759-!Fg1L6t&6lB&new=sjss22%@%E2%82%AC55jaJasj!.k&repeat=sjss22%@%E2%82%AC55jaJasj!.k8 HTTP/1.1" 401 39 "http://localhost:3000/" "Mozilla/5.0 (Linux; Android 8.1.0; Nexus 5X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 Mobile Safari/537.36"```
        - 重复新密码时，两次不匹配，响应 401。密码为旧密码
            ```0Y8rMnww$*9VFYE%C2%A759-!Fg1L6t&6lB```
            - URL 解码
                ```0Y8rMnww$*9VFYEÂ§59-!Fg1L6t&6lB```
            - ```Â``` 字符在发送转换时可能出错，确保此字符包含在内
            - 使用重置密码功能，设置此字符串为新密码，根据 SQL 注入得到的用户表信息检索匹配用户
                ```json
                {
                    "username": "",
                    "email": "J12934@juice-sh.op",
                    "password": "3c2abc04e4a6ea8f1327d0aae3714b7d",
                    "deletedAt": null
                }
                ```
            - 使用邮箱与明文密码登录账户