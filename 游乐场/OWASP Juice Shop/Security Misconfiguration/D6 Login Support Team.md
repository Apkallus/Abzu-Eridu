---
title: Login Support Team
description: 信息收集发现特定程序的被加密的密码文件，推测其中包含支持团队的密码。在前端代码中发现支持团队的密码规则，使用爆破脚本设置密码规则爆破密码文件
---

- 描述：使用支持团队的原用户凭证登录，而不应用SQL注入或任何其他绕过方法。
- 查找 SQL 注入得到的用户表或 SQL 注入登录账户得到的 JWT
    得到密码的 MD5 hash 字符串
    ```json
    "email": "support@juice-sh.op",
    "password": "3869433d74e3d0c86fd25562f836bc82"
    ```
    彩虹表得到明文
    ```J6aVjTgOpRs@?5l!Zkq2AYnCE@RF$P```
    - 但此挑战拥有 D6 难度，应该是用其他方法

- 在 ```main.js``` 中搜索 ```support```
    - 得到对于 support 邮件地址的特殊密码强度规则
    ```javascript
    changePassword() {
            localStorage.getItem("email")?.match(/support@.*/) && !this.newPasswordControl.value.match(/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,30}/) && console.error("Parola echipei de asisten\u021b\u0103 nu respect\u0103 politica corporativ\u0103 pentru conturile privilegiate! V\u0103 rug\u0103m s\u0103 schimba\u021bi parola \xeen consecin\u021b\u0103!"), this.userService.changePassword({
                current: this.passwordControl.value,
                new: this.newPasswordControl.value,
                repeat: this.repeatNewPasswordControl.value
            })
    ```
:x: 未完成
- 查看示例解决方案：
    1. 此处使用挑战 Access Log 相关的 ```/ftp/incident-support.kdbx``` 文件
    2. 下载对应软件
    3. 在 ```main.js``` 中查看修改 support 账户密码的正则表达式规则
    4. 在爆破脚本或工具中应用密码强度规则暴力破解密码
    5. 攻破文件后在对应项右键复制密码
- python 拥有对应的库，在已知密码规则的情况下如何微调爆破单词表？