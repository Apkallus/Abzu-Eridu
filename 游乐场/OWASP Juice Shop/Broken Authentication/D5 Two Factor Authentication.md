---
title: Two Factor Authentication
description: pass
---

- 描述：为用户"wurstbrot"解决双因素认证挑战。（禁用、绕过或覆盖他的双因素认证设置不被视为解决方案）

- SQL 注入用户表查询
    ```json
    {
        "username": "wurstbrot",
        "email": "wurstbrot@juice-sh.op",
        "password": "9ad5b0492bbe528583e128d2a8941de4",
        "deletedAt": null,
        "totpSecret": "IFTXE3SPOEYVURT2MRYGI52TKJ4HC3KH"
    }
    ```

- 查看示例解决方案：对可能的列名进行探测。但此处由 SQL 注入得到的表规范的元数据或 JWT，已确认所有字段信息与值

- 实际上只是下载双因素验证应用，手动输入秘密字符串，最后后在登录时使用即可